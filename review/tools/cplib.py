# Round-closure + stated-count checks on parsed CrochetPARADE rows (output of rows.mjs).
import json,re,collections,subprocess,os
from pathlib import Path
from tempfile import TemporaryDirectory
NONST={'ss','tie up stitches','ring','sk','ssbl','ssfl'}
NODE=os.environ.get('NODE','node')
HERE=os.path.dirname(os.path.abspath(__file__))
def parse_all(patterns,tag='tmp'):
    """patterns: {key:{'dsl':..}} -> parsed rows dict (runs the real CrochetPARADE parser)."""
    with TemporaryDirectory(prefix=f'crochetparade-{tag}-') as directory:
        input_path = Path(directory, 'input.json')
        output_path = Path(directory, 'output.json')
        input_path.write_text(json.dumps(patterns), encoding='utf-8')
        subprocess.run([NODE, os.path.join(HERE, 'rows.mjs'), input_path, output_path],
                       check=True, stdout=subprocess.DEVNULL)
        return json.loads(output_path.read_text(encoding='utf-8'))
def codelines(s):
    out=[];pend=None
    for i,l in enumerate(s.split('\n')):
        c=re.sub(r'#.*','',l).strip()
        if not c: continue
        if c.startswith('DEF') or re.fullmatch(r'\$.*\$',c): continue
        if pend is not None: out[-1]=(out[-1][0],out[-1][1]+' '+c,out[-1][2]+[i])
        else: out.append((i,c,[i]))
        pend=True if c.endswith('...') else None
    return out
def stated(lines,i):
    cands=[]
    m=re.search(r'#(.*)',lines[i])
    if m: cands.append(m.group(1))
    j=i-1
    if j>=0 and lines[j].strip().startswith('#'): cands.append(lines[j].strip()[1:])
    for c in cands:
        m=re.search(r'(?:^|[.:;(\[=]|--|→|->)\s*\(?(\d+)\s+(sc|sts|st|hdc|dc|stitches)\s*[.)\]]*\s*$',c.strip(),re.I)
        if m: return int(m.group(1)),c.strip()[:160]
    return None
def analyze_one(v,text):
    if 'rows' not in v: return {'error':v['error'].split('\n')[0]}
    lines=text.split('\n'); cl=codelines(text); rows={r['n']:r for r in v['rows']}; n=max(rows)+1
    R={'mapped':n==len(cl),'flags':[],'nrows':n,'checked':0,'stated_ok':0,'stated_bad':0,'rowinfo':{}}
    idrow={}; carry=[]
    for i in range(n):
        r=rows.get(i)
        if r is None: continue
        r['_bonus']=list(carry); r['_made']=[]; carry=[]
        for t,ids,att,ex in r['st']:
            if t=='start a new chain': r['_bonus']+=ids
            elif t not in NONST: r['_made']+=ids
        only=set(r['types'])
        if only<={'start a new chain'}: carry=r['_bonus']; r['_skip']=True; continue
        for x in r['_made']+r['_bonus']: idrow[x]=i
        for t,ids,att,ex in r['st']:
            for x in ids: idrow.setdefault(x,i)
    prev=None
    for i in range(n):
        r=rows.get(i)
        if r is None or r.get('_skip'): prev=None; continue
        types=r['types']
        if set(types)<={'tie up stitches'}: prev=None; continue
        newpiece='start a new chain' in types or 'ring' in types or prev is None or not prev['_made']
        imp=[]; alltg=set(); nex=0
        for t,ids,att,ex in r['st']:
            alltg.update(att)
            if ex: nex+=1
            elif t!='sk': imp+=[(t,a) for a in att]
        off=collections.Counter()
        for t,a in imp:
            tr=idrow.get(a)
            if tr!=i-1 and prev is not None: off['self' if tr==i else (tr-i if tr is not None else '?')]+=1
        left=None
        if prev is not None and not newpiece: left=len([x for x in prev['_made'] if x not in alltg])
        made=len(r['_made']); mch=types.get('ch',0)
        st=stated(lines,cl[i][0]) if (R['mapped'] and 'ring' not in types and made) else None
        f={}
        if not newpiece:
            R['checked']+=1
            if off: f['off']={str(a):b for a,b in off.items()}
            if left: f['left']=left
        if st:
            if st[0] in (made,made-mch): R['stated_ok']+=1
            else: R['stated_bad']+=1; f['stated']=st[0]; f['comment']=st[1]
        R['rowinfo'][i]={'made':made,'prev':len(prev['_made']) if prev else None,'new':newpiece,'stated':st[0] if st else None}
        if f:
            code=cl[i][1] if R['mapped'] else ''
            if 'stated' in f or 'off' in f: f['sev']='count'
            elif re.search(r'turn\s*$',code) or (prev and re.search(r'turn\s*$',cl[i-1][1] if R['mapped'] else '')): f['sev']='partial_row'
            elif re.fullmatch(r'\w*\d+tog(\.\w+)?',code.strip()): f['sev']='closing'
            elif nex and not re.fullmatch(r'.*ss@\[%,0\]\s*',code) or len(re.findall('@',code))>1: f['sev']='explicit'
            else: f['sev']='count'
            f.update(row=i,line=cl[i][0] if R['mapped'] else None,code=cl[i][1][:90] if R['mapped'] else '',made=made,ch=mch,prev=len(prev['_made']) if prev else None,explicit=nex,prevcode=(cl[i-1][1][:70] if R['mapped'] and i>0 else ''))
            R['flags'].append(f)
        prev=r
    return R
