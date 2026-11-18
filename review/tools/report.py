# usage: report.py patterns.json out_flags.json  -> parse + analyze, write flags, print summary
import json,sys,collections
from cplib import *
src=json.load(open(sys.argv[1])); P=parse_all(src,'rep'); res={}
for k,v in src.items(): res[k]=analyze_one(P[k],v['dsl']); res[k]['confidence']=v['confidence']
json.dump(res,open(sys.argv[2],'w'))
tot=collections.Counter(); sev=collections.Counter(); T=collections.Counter()
for k,v in res.items():
    if 'error' in v: tot['error']+=1; continue
    for x in('checked','stated_ok','stated_bad'): T[x]+=v[x]
    s={f['sev'] for f in v['flags']}
    for f in v['flags']: sev[f['sev']]+=1
    tot['unmapped' if not v['mapped'] else 'clean' if not v['flags'] else 'count_issue' if 'count' in s else 'info_only']+=1
print(tot,sev,T)
