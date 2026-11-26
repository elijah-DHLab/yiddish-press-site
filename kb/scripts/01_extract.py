#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Step 1: extract every entity surface form + article contexts from data.json
into kb/work/ so they can be clustered and resolved.

Outputs
  kb/work/articles.jsonl        one article per line: id, date, paper, summary, context, entity lists
  kb/work/mentions_<t>.tsv      key<TAB>display<TAB>variants<TAB>yiddish<TAB>count<TAB>first<TAB>last<TAB>article ids
  kb/work/batch_<t>_<n>.tsv     the same rows, split into work batches
"""
import json, collections, os, sys, math
sys.path.insert(0, os.path.dirname(__file__))
from kblib import *

BATCH = {'ppl': 3, 'pl': 2, 'org': 2, 'grp': 1, 'top': 1}

D = load_json(os.path.join(ROOT, 'data.json'))
A = D['arts']
os.makedirs(WORK, exist_ok=True)

with open(os.path.join(WORK, 'articles.jsonl'), 'w', encoding='utf-8') as f:
    for a in A:
        f.write(json.dumps(dict(id=a['id'], d=a['d'], p=a['p'], s=a['s'], c=a['c'][:500],
                                **{t: [h + (' (' + y + ')' if y else '') for h, y in a[t]] for t in TYPES}),
                           ensure_ascii=False) + '\n')

for t in TYPES:
    disp = collections.defaultdict(collections.Counter)
    yid = collections.defaultdict(collections.Counter)
    arts = collections.defaultdict(list)
    for a in A:
        seen = set()
        for h, y in a[t]:
            k = norm_key(h)
            if not k: continue
            disp[k][h] += 1
            if y: yid[k][y] += 1
            if k not in seen: seen.add(k); arts[k].append(a)
    rows = []
    for k, c in disp.items():
        al = arts[k]
        rows.append([k, c.most_common(1)[0][0], ' | '.join(x for x, _ in c.most_common()[1:]),
                     ' | '.join(x for x, _ in yid[k].most_common(4)), str(len(al)),
                     min(a['d'] for a in al), max(a['d'] for a in al), ' '.join(a['id'] for a in al[:6])])
    # sort: people by last token (surname) so variants sit together; others by key
    if t == 'ppl': rows.sort(key=lambda r: (r[0].split(' ')[-1], r[0]))
    else: rows.sort(key=lambda r: r[0])
    head = 'key\tdisplay\tvariants\tyiddish\tcount\tfirst\tlast\tarticle_ids\n'
    with open(os.path.join(WORK, f'mentions_{t}.tsv'), 'w', encoding='utf-8') as f:
        f.write(head); f.writelines('\t'.join(r) + '\n' for r in rows)
    n = BATCH[t]; size = math.ceil(len(rows) / n)
    for i in range(n):
        with open(os.path.join(WORK, f'batch_{t}_{i + 1}.tsv'), 'w', encoding='utf-8') as f:
            f.write(head); f.writelines('\t'.join(r) + '\n' for r in rows[i * size:(i + 1) * size])
    print(t, len(rows), 'keys ->', n, 'batches')
