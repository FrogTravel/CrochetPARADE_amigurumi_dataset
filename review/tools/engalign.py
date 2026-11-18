# English stated-count sequence vs CP per-row made counts: ordered-subsequence coverage (LCS)
import re
def eng_counts(eng):
    out=[]
    for l in eng.split('\n'):
        t=l.strip()
        m=re.search(r'(?:^|[^A-Za-z0-9\s])\s*[\[(]?(\d+)\s+(sc|sts|st|hdc|dc|stitches)\s*[.)\]*]*\s*$',t,re.I)
        if m: out.append(int(m.group(1)))
    return out
def lcs(a,b):
    n,m=len(a),len(b)
    if not n or not m: return 0
    prev=[0]*(m+1)
    for i in range(n):
        cur=[0]*(m+1); ai=a[i]
        for j in range(m):
            cur[j+1]=prev[j]+1 if ai==b[j] else (prev[j+1] if prev[j+1]>cur[j] else cur[j])
        prev=cur
    return prev[m]
def coverage(eng,made_seq):
    e=eng_counts(eng)
    if not e: return None
    return {'english_counts':len(e),'matched_in_order':lcs(e,made_seq)}

def _norm(s): return re.sub(r'[^a-z0-9]+',' ',s.lower()).strip()
def eng_round_lines(eng):
    out=[]
    for l in eng.split('\n'):
        t=l.strip().lstrip('*').strip()
        if re.match(r'(\d+(st|nd|rd|th)\b.*?(rnd|row|round)s?\b|next (rnd|row|round)|rnds? \d+|rows? \d+|round \d+|row \d+)',t,re.I): out.append(t)
    return out
def quote_coverage(eng,dsl):
    """share of English round/row lines whose opening words are quoted in a CP comment"""
    rl=eng_round_lines(eng)
    if not rl: return None
    com=_norm(' \n '.join(re.findall(r'#(.*)',dsl)))
    hit=0
    for t in rl:
        body=_norm(re.sub(r'^.*?:','',t,count=1))  # text after "3rd rnd:"
        key=' '.join(body.split()[:6])
        if len(key)>=12 and key in com: hit+=1
    return {'english_round_lines':len(rl),'quoted_in_comments':hit}
def stitch_profile(text):
    t=text.lower(); return {s:len(re.findall(r'(?<![a-z])'+s+r'(?![a-z])',t)) for s in ('sc','hdc','dc','tr')}
