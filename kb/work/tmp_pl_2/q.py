import sys,json,os
sys.path.insert(0,'kb/scripts')
from kblib import norm_key, split_item
sys.stdout.reconfigure(encoding='utf-8')
keys=[l.strip() for l in open(sys.argv[1],encoding='utf-8') if l.strip()]
N=int(sys.argv[2]) if len(sys.argv)>2 else 2
idx={}
for l in open('kb/work/articles.jsonl',encoding='utf-8'):
    a=json.loads(l)
    for x in a['pl']:
        k=norm_key(split_item(x)[0]); idx.setdefault(k,[]).append((a,x))
for k in keys:
    print('##',k)
    for a,x in idx.get(k,[])[:N]:
        pls=[p.split(' (')[0] for p in a['pl']][:6]
        print('  ',a['id'],a['d'],x,'|',a["s"][:120],'| PL:',', '.join(pls))
