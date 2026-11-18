# usage: normalize2.py norm.json out.json — mechanical compile repairs: unbalanced brackets inside comments; truncated final line
import json,sys,re
src=json.load(open(sys.argv[1])); fl=json.load(open(sys.argv[1]+'.flags')); out={}; n=0; log={}
def bal(c):
    d={'(':0,'[':0,'{':0}; pairs={')':'(',']':'[','}':'{'}
    st=[]
    for ch in c:
        if ch in d: st.append(ch)
        elif ch in pairs:
            if not st or st[-1]!=pairs[ch]: return False
            st.pop()
    return not st
for k,v in src.items():
    lines=v['dsl'].split('\n'); L=[]
    if 'truncated_output' in fl[k]:
        while lines and not lines[-1].strip(): lines.pop()
        L.append(('dropped_truncated_last_line',lines.pop()))
        while lines and (not lines[-1].strip() or lines[-1].strip().startswith('#')): lines.pop()
    for i,l in enumerate(lines):
        if '#' in l:
            a,b=l.split('#',1)
            if not bal(b):
                nb=re.sub(r'[()\[\]{}]','',b); lines[i]=a+'#'+nb; L.append(('comment_brackets',i))
    out[k]=dict(v,dsl='\n'.join(lines)+('\n' if lines else ''))
    if L: log[k]=L
json.dump(out,open(sys.argv[2],'w')); json.dump(log,open(sys.argv[2]+'.log','w'))
print('patterns touched',len(log),'comment lines',sum(1 for x in log.values() for y in x if y[0]=='comment_brackets'))
