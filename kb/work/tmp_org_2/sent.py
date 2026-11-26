import sys, os, json, re
sys.path.insert(0, 'kb/scripts')
from kblib import *
sys.stdout.reconfigure(encoding='utf-8')
arts=[json.loads(l) for l in open('kb/work/articles.jsonl',encoding='utf-8')]
idx={}
for a in arts:
    for x in a['org']:
        idx.setdefault(norm_key(split_item(x)[0]),[]).append((a,x))
key=sys.argv[1]; stems=sys.argv[2].split('|')
for a,x in idx.get(key,[]):
    text=a['s']+' '+a['c']
    sents=re.split(r'(?<=[.:;])\s+',text)
    hits=[s for s in sents if any(st in s for st in stems)]
    out=' // '.join(h[:200] for h in hits) if hits else '-- '+a['s'][:120]
    print(a['id'],a['d'],'|',out,'| ORG:',';'.join(o.split(' (')[0] for o in a['org'] if o!=x)[:120])
