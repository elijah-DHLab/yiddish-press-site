import sys, os, json, re
sys.path.insert(0, 'kb/scripts')
from kblib import *
sys.stdout.reconfigure(encoding='utf-8')
arts = {}
idx = {}
for l in open('kb/work/articles.jsonl', encoding='utf-8'):
    a = json.loads(l); arts[a['id']] = a
    for x in a['ppl']:
        idx.setdefault(norm_key(split_item(x)[0]), []).append(a['id'])
rows = [l.split('\t') for l in open('kb/work/batch_ppl_2.tsv', encoding='utf-8').read().splitlines()[1:]]
lo, hi = int(sys.argv[1]), int(sys.argv[2])
KNOWN=set(map(int,open('kb/work/tmp_ppl_2/known.txt').read().split()))
maxa = int(sys.argv[3]) if len(sys.argv) > 3 else 2
for i, r in enumerate(rows, 1):
    if not (lo <= i <= hi) or i in KNOWN: continue
    k = r[0]
    print(f'## {i} {k}')
    stem = k.split()[-1]
    for aid in idx.get(k, [])[:maxa]:
        a = arts[aid]
        txt = a['s'] + ' ' + a.get('c', '')
        m = None
        for L in (len(stem), 4, 3):
            if L > len(stem): continue
            p = txt.find(stem[:L]) if L >= 3 else -1
            if p >= 0: m = p; break
        if m is not None:
            snip = txt[max(0, m - 60): m + 70]
        else:
            snip = a["s"][:150]
        co = [split_item(x)[0] for x in a['ppl'] if norm_key(split_item(x)[0]) != k][:3]
        print(f"  {aid} {a['d']} | {snip} || co: {', '.join(co)}")
