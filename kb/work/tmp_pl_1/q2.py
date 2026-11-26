import sys, os, json, re
sys.path.insert(0, 'kb/scripts')
from kblib import *
sys.stdout.reconfigure(encoding='utf-8')
arts = [json.loads(l) for l in open('kb/work/articles.jsonl', encoding='utf-8')]
idx = {}
for a in arts:
    for x in a['pl']:
        idx.setdefault(norm_key(split_item(x)[0]), []).append((a, x))
for k in sys.argv[1:]:
    for a, x in idx.get(k, [])[:int(os.environ.get('M','1'))]:
        s = a['s']+' '+(a.get('c') or '')
        # find sentence with key stem
        stem = k[:3]
        i = s.find(stem)
        snip = s[max(0,i-120):i+150] if i>=0 else s[:200]
        print('##', k, '|', a['id'], a['d'], '|', snip.replace('\n',' '), '|PL:', ', '.join(split_item(y)[0] for y in a['pl'][:12]))
