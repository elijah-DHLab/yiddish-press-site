import sys, os, json
sys.path.insert(0, 'kb/scripts')
from kblib import *
sys.stdout.reconfigure(encoding='utf-8')
arts = {}
for l in open(os.path.join(WORK,'articles.jsonl'),encoding='utf-8'):
    a=json.loads(l); arts[a['id']]=a
rows={}
for l in open('kb/work/tbatch_1.tsv',encoding='utf-8').read().splitlines()[1:]:
    c=l.split('\t'); rows[c[0]]=c[4].split()
keys=[k.strip() for k in open(sys.argv[1],encoding='utf-8') if k.strip()]
n=int(sys.argv[2]) if len(sys.argv)>2 else 170
for k in keys:
    ids=rows.get(k)
    if ids is None: print('MISSING',k); continue
    a=arts.get(ids[0])
    print(f"## {k} | {a['d']} | {a['s'][:n]}")
