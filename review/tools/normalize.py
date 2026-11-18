# usage: normalize.py in.json out.json  -> strips markdown fences / prose preamble; records flags
import json,sys,re
src=json.load(open(sys.argv[1])); out={}; flags={}
for k,v in src.items():
    s=v['dsl']; f=[]
    if '```' in s:
        n=s.count('```'); i=s.index('```')
        if s[:i].strip(): f.append('prose_preamble')
        body=s[i+3:]
        body=body[body.index('\n')+1:] if '\n' in body else ''
        if n>=2:
            body=body[:body.rindex('```')]
        else:
            f.append('truncated_output')
        f.append('fenced'); s=body.strip('\n')+'\n'
    out[k]=dict(v,dsl=s); flags[k]=f
json.dump(out,open(sys.argv[2],'w')); json.dump(flags,open(sys.argv[2]+'.flags','w'))
import collections; print(collections.Counter(x for f in flags.values() for x in f))
print(collections.Counter(v.get('tokens_out') for k,v in src.items() if 'truncated_output' in flags[k]))
