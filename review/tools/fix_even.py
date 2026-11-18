# usage: fix_even.py in.json out.json log.json — corroborated repair of plain "work even" round counts
import json,sys,re,collections
from cplib import *
src=json.load(open(sys.argv[1])); cur={k:dict(v) for k,v in src.items()}
EVEN=re.compile(r'^(\s*)(\d+)((?:sc|hdc|dc|scbl|scfl|hdcbl|hdcfl|dcbl|dcfl)\s*(?:,\s*ss@\[%,0\])?\s*(?:#.*)?)$')
log=collections.defaultdict(list)
dirty=set(cur)
parsed={}
for it in range(6):
    parsed.update(parse_all({k:cur[k] for k in dirty},'fe')); dirty=set(); cand={}; meta={}
    for k,v in cur.items():
        A=analyze_one(parsed[k],v['dsl'])
        if 'error' in A or not A['mapped'] or not A['flags']: continue
        cl=codelines(v['dsl']); lines=v['dsl'].split('\n'); flagged={f['row']:f for f in A['flags']}
        changes=[]; ri=A['rowinfo']
        for f in A['flags']:
            i=f['row']
            if 'stated' in f and 'left' not in f and 'off' not in f: continue
            m=EVEN.match(lines[cl[i][0]])
            if not m or len(cl[i][2])>1: continue
            if (i-1) in flagged: continue   # previous row itself suspect
            target=f['prev']
            if target is None or target==int(m.group(2)) or target<=0: continue
            st=ri[str(i)]['stated'] if str(i) in ri else ri[i]['stated']
            if st is not None and st!=target: continue
            # cascade over following identical even rows
            old=int(m.group(2)); j=i; ch=[]
            while j<len(cl):
                mj=EVEN.match(lines[cl[j][0]])
                if not mj or int(mj.group(2))!=old or len(cl[j][2])>1: break
                sj=ri.get(j,{}).get('stated')
                if sj is not None and sj!=target: break
                ch.append((cl[j][0],old,target)); j+=1
            changes=ch; break   # one cascade per pattern per iteration
        if changes:
            nl=list(lines)
            for ln,old,new in changes:
                m=EVEN.match(nl[ln]); nl[ln]=m.group(1)+str(new)+m.group(3)
            cand[k]=dict(v,dsl='\n'.join(nl)); meta[k]=(changes,len(A['flags']),{f['row'] for f in A['flags']})
    if not cand: break
    p2=parse_all(cand,'fe2'); acc=0
    for k,c in cand.items():
        A2=analyze_one(p2[k],c['dsl'])
        if 'error' in A2: continue
        changes,nold,oldset=meta[k]
        newset={f['row'] for f in A2['flags']}
        if len(newset)<nold and newset<=oldset:
            cur[k]=c; acc+=1; dirty.add(k); log[k]+= [{'line':ln,'old':o,'new':n} for ln,o,n in changes]
    print('iter',it,'candidates',len(cand),'accepted',acc)
    if not acc: break
json.dump(cur,open(sys.argv[2],'w')); json.dump(log,open(sys.argv[3],'w'))
print('patterns changed',len(log),'lines changed',sum(len(x) for x in log.values()))
