import sys, json, re
sys.path.insert(0,'kb/scripts')
from kblib import *
sys.stdout.reconfigure(encoding='utf-8')
arts=[json.loads(l) for l in open('kb/work/articles.jsonl',encoding='utf-8')]
k=sys.argv[1]; pat=sys.argv[2]
for a in arts:
    if any(norm_key(split_item(x)[0])==k for x in a['ppl']):
        t=a['s']+' || '+a.get('c','')
        ms=[t[max(0,m.start()-90):m.start()+90] for m in re.finditer(pat,t)][:2]
        print(a['id'],a['d'],'|', ' ... '.join(ms) if ms else t[:180])
