import sys,json,re
sys.path.insert(0,'kb/scripts')
from kblib import *
sys.stdout.reconfigure(encoding='utf-8')
k=sys.argv[1]
for l in open('kb/work/articles.jsonl',encoding='utf-8'):
    a=json.loads(l)
    for x in a['grp']:
        h,y=split_item(x)
        if norm_key(h)==k:
            t=a['s']+' '+a.get('c','')
            sn=[t[max(0,m.start()-40):m.end()+40] for m in re.finditer('ספרד',t)][:3]
            print(a['id'],'|',x,'|',' ;; '.join(sn) or a['s'][:150])
