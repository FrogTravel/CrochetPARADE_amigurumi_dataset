#!/usr/bin/env python3
# usage: python3 check.py path/to/pattern.cp   -> compiles with the real CrochetPARADE parser and prints round-closure flags
import sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from cplib import *
p=sys.argv[1]; text=open(p).read(); tag='chk%d'%os.getpid()
P=parse_all({'x':{'dsl':text,'confidence':None}},tag)
if 'error' in P['x']:
    print('COMPILE ERROR:'); print(P['x']['error'][:1500]); sys.exit(1)
A=analyze_one(P['x'],text)
for m in P['x']['msgs']: print('parser message:',m[:300].replace('\n',' / '))
if not A['mapped']: print('WARNING: could not map parser rows to file lines (line numbers unavailable)')
print(f"compiled OK: {A['nrows']} rows, {A['checked']} continuation rows checked, stated counts ok={A['stated_ok']} bad={A['stated_bad']}")
fl=A['flags']; cnt=[f for f in fl if f['sev']=='count']; oth=[f for f in fl if f['sev']!='count']
def show(f):
    bits=[]
    if 'left' in f: bits.append(f"leaves {f['left']} of the previous row's {f['prev']} stitches unworked")
    if 'off' in f: bits.append('works past the previous row: '+', '.join(f"{n} stitch(es) attach to {'this same row' if a=='self' else 'row offset '+a}" for a,n in f['off'].items()))
    if 'stated' in f: bits.append(f"makes {f['made']} but the comment states {f['stated']} ({f['comment'][:90]})")
    print(f"  line {f['line']+1 if f['line'] is not None else '?'} [{f['sev']}] `{f['code']}` (prev row {f['prev']} sts, makes {f['made']}): "+'; '.join(bits))
print(f"COUNT FLAGS: {len(cnt)}"); [show(f) for f in cnt]
print(f"INFO FLAGS (partial rows / explicit attachments / closing; usually intentional): {len(oth)}"); [show(f) for f in oth]
