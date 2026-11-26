import sys, os, json
sys.path.insert(0, 'kb/scripts')
from kblib import *
sys.stdout.reconfigure(encoding='utf-8')
arts=[json.loads(l) for l in open('kb/work/articles.jsonl',encoding='utf-8')]
idx={}
for a in arts:
    for x in a['org']:
        idx.setdefault(norm_key(split_item(x)[0]),[]).append((a,x))
n=int(os.environ.get('N','220'))
for k in sys.argv[1:]:
    print('###',k)
    for a,x in idx.get(k,[]):
        print(' ',a['id'],a['d'],'|',x,'|',a['s'][:n],'| PL:',','.join(p.split(' (')[0] for p in a['pl'][:6]))
