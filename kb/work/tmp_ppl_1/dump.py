import sys, os, json, re
sys.path.insert(0, 'kb/scripts')
from kblib import *
sys.stdout.reconfigure(encoding='utf-8')
arts = [json.loads(l) for l in open('kb/work/articles.jsonl', encoding='utf-8')]
idx = {}
for a in arts:
    for x in a['ppl']:
        idx.setdefault(norm_key(split_item(x)[0]), []).append(a)
rows = [l.split('\t') for l in open('kb/work/batch_ppl_1.tsv', encoding='utf-8').read().splitlines()[1:]]
lo, hi = int(sys.argv[1]), int(sys.argv[2])
for i, r in enumerate(rows[lo:hi], lo+1):
    key = r[0]
    toks = [t for t in re.split(r'[\s(),]+', key) if len(t) > 2]
    print(f'## {i} {key} [{r[3]}]')
    for a in idx.get(key, [])[:4]:
        txt = a['s'] + ' ' + a.get('c', '')
        snip = None
        for t in reversed(toks):
            m = txt.find(t)
            if m >= 0:
                snip = txt[max(0, m-70): m+90]; break
        if snip is None: snip = a['s'][:70] + ' || ppl: ' + '; '.join(x.split(' (')[0] for x in a['ppl'][:8])
        print(f"  {a['id']} {a['d']}: {snip.replace(chr(10),' ')}")
