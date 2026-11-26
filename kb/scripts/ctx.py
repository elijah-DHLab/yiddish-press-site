#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Show the articles in which a surface form occurs (for disambiguation).

  python kb/scripts/ctx.py ppl "סולטאן"        # type + key (key as in the batch TSV, 1st column)
  python kb/scripts/ctx.py ppl "סולטאן" --short  # one line per article
  python kb/scripts/ctx.py art hyt19120404-01.2.14   # one article in full
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))
from kblib import *
if hasattr(sys.stdout, 'reconfigure'): sys.stdout.reconfigure(encoding='utf-8')

arts = [json.loads(l) for l in open(os.path.join(WORK, 'articles.jsonl'), encoding='utf-8')]
t, key = sys.argv[1], sys.argv[2]
short = '--short' in sys.argv
if t == 'art':
    for a in arts:
        if a['id'] == key: print(json.dumps(a, ensure_ascii=False, indent=1))
    sys.exit()
hits = [a for a in arts if any(norm_key(split_item(x)[0]) == key for x in a[t])]
print(f'{len(hits)} articles for {t}:{key}')
for a in hits:
    if short:
        print(f"{a['id']}\t{a['d']}\t{a['s'][:160]}")
    else:
        print(f"\n== {a['id']}  {a['d']}  {a['p']}\n  summary: {a['s'][:400]}")
        for tt in ('ppl', 'pl', 'org', 'top'):
            print(f'  {tt}: ' + ' ; '.join(a[tt][:12]))
