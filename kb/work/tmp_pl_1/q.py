import sys, os, json
sys.path.insert(0, 'kb/scripts')
from kblib import *
sys.stdout.reconfigure(encoding='utf-8')
n = int(os.environ.get('N', '220'))
arts = [json.loads(l) for l in open('kb/work/articles.jsonl', encoding='utf-8')]
idx = {}
for a in arts:
    for x in a['pl']:
        idx.setdefault(norm_key(split_item(x)[0]), []).append((a, x))
for k in sys.argv[1:]:
    print('##', k)
    for a, x in idx.get(k, [])[:int(os.environ.get('M','3'))]:
        c = a.get('c') or ''
        print('  ', a['id'], a['d'], '|', x, '|', (a['s'][:n]), '|C:', c[:n], '|PL:', ', '.join(split_item(y)[0] for y in a['pl'][:10]))
