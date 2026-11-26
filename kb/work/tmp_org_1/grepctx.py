import sys, json, re
sys.path.insert(0,'kb/scripts')
from kblib import *
sys.stdout.reconfigure(encoding='utf-8')
key=sys.argv[1]; pat=sys.argv[2] if len(sys.argv)>2 else None
for l in open('kb/work/articles.jsonl',encoding='utf-8'):
    a=json.loads(l)
    if any(norm_key(split_item(x)[0])==key for x in a['org']):
        txt=a['s']+' || '+(a.get('c') or '')
        snips=[]
        if pat:
            for m in re.finditer(pat, txt):
                snips.append(txt[max(0,m.start()-120):m.end()+80])
        pls=[split_item(x)[0] for x in a['pl']][:10]
        print(a['id'],a['d'],'|PL:',','.join(pls))
        for s in snips: print('    >>',s)
