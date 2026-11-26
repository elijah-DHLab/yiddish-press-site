import sys, json
sys.path.insert(0,'kb/scripts')
from kblib import *
sys.stdout.reconfigure(encoding='utf-8')
arts=[json.loads(l) for l in open('kb/work/articles.jsonl',encoding='utf-8')]
for k in sys.argv[1:]:
    print('##',k)
    for a in arts:
        if any(norm_key(split_item(x)[0])==k for x in a['ppl']):
            print(' ',a['id'],a['d'],'|',' ; '.join(a['ppl'][:14])[:330])
