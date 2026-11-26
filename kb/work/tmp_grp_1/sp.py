import sys,json,re
sys.path.insert(0,'kb/scripts')
from kblib import *
sys.stdout.reconfigure(encoding='utf-8')
targets=sys.argv[1:]
for l in open('kb/work/articles.jsonl',encoding='utf-8'):
    a=json.loads(l)
    for x in a['grp']:
        h,y=split_item(x)
        if norm_key(h) in targets:
            print(a['id'],a['d'],'|',x,'|',a['s'][:230],'| grp:',', '.join(a['grp'][:12]))
