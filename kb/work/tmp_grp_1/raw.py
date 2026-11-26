import sys,json,re
sys.path.insert(0,'kb/scripts')
from kblib import *
sys.stdout.reconfigure(encoding='utf-8')
ks=sys.argv[1:]
for l in open('kb/work/articles.jsonl',encoding='utf-8'):
    a=json.loads(l)
    for x in a['grp']:
        h,y=split_item(x)
        if norm_key(h) in ks:
            print(norm_key(h),'|',a['id'],'|',x,'|',a.get('c','')[:200])
