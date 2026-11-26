#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validate an entity-resolution output file against its batch.

  python kb/scripts/validate.py kb/work/ent_pl_1.json kb/work/batch_pl_1.tsv
  python kb/scripts/validate.py kb/work/topicmap_1.json kb/work/tbatch_1.tsv --topics
"""
import sys, os, json, re, collections
sys.path.insert(0, os.path.dirname(__file__))
from kblib import *
if hasattr(sys.stdout, 'reconfigure'): sys.stdout.reconfigure(encoding='utf-8')

path, batch = sys.argv[1], sys.argv[2]
topics = '--topics' in sys.argv
src_type = re.search(r'batch_(\w+?)_\d', os.path.basename(batch))
src_type = src_type.group(1) if src_type else 'top'
keys = [l.split('\t')[0] for l in open(batch, encoding='utf-8').read().splitlines()[1:] if l.strip()]
keyset = set(keys)
errs, warns = [], []
try:
    data = json.load(open(path, encoding='utf-8'))
except Exception as e:
    print('JSON ERROR:', e); sys.exit(1)

ID = re.compile(r'^(ppl|pl|org|grp|ev|top):[a-z0-9][a-z0-9-]*$')
arts = {}
for l in open(os.path.join(WORK, 'articles.jsonl'), encoding='utf-8'):
    a = json.loads(l)
    for x in a[src_type]:
        arts.setdefault(norm_key(split_item(x)[0]), set()).add(a['id'])

covered = collections.Counter()
if topics:
    vocab = load_json(os.path.join(WORK, 'vocab.json'), {})
    vids = {c['id'] for c in vocab.get('concepts', [])} | {e['id'] for e in vocab.get('events', [])}
    m = data.get('map', {})
    for k, ids in m.items():
        if k not in keyset: errs.append(f'key not in batch: {k}')
        if not isinstance(ids, list): errs.append(f'{k}: value must be a list'); continue
        for i in ids:
            if i not in vids and not ID.match(i): errs.append(f'{k}: bad id {i}')
            elif i not in vids and not i.startswith(('pl:', 'ppl:', 'org:', 'grp:')): errs.append(f'{k}: id not in vocab.json: {i}')
        covered[k] += 1
else:
    seen = set()
    for e in data.get('entities', []):
        if not ID.match(e.get('id', '')): errs.append(f"bad id: {e.get('id')}")
        if e.get('id') in seen: errs.append(f"duplicate id: {e['id']}")
        seen.add(e.get('id'))
        if not e.get('he'): errs.append(f"{e.get('id')}: missing he")
        if not e.get('keys'): warns.append(f"{e.get('id')}: no keys")
        for k in e.get('keys', []):
            if k not in keyset: errs.append(f"{e['id']}: key not in batch: {k!r}")
            covered[k] += 1
        for f in ('parent', 'country'):
            v = e.get(f)
            if v and not ID.match(v): errs.append(f"{e['id']}: bad {f} {v}")
    for c in data.get('contextual', []):
        k = c.get('key')
        if k not in keyset: errs.append(f'contextual key not in batch: {k!r}')
        covered[k] += 1
        for aid, eid in (c.get('articles') or {}).items():
            if aid not in arts.get(k, set()): errs.append(f'contextual {k}: article {aid} does not contain this key')
            if eid is not None and not ID.match(eid): errs.append(f'contextual {k}: bad id {eid}')
        missing = arts.get(k, set()) - set((c.get('articles') or {}).keys())
        if missing: errs.append(f'contextual {k}: articles not resolved: {sorted(missing)}')
    for d in data.get('drop', []):
        k = d.get('key') if isinstance(d, dict) else d
        if k not in keyset: errs.append(f'drop key not in batch: {k!r}')
        covered[k] += 1

missing = [k for k in keys if not covered[k]]
if missing: errs.append(f'{len(missing)} batch keys not covered, e.g.: ' + ' | '.join(missing[:25]))
for w in warns[:20]: print('warn:', w)
for e in errs[:80]: print('ERROR:', e)
if len(errs) > 80: print(f'... and {len(errs) - 80} more errors')
n_ent = len(data.get('entities', [])) if not topics else len(data.get('map', {}))
print(f'{"OK" if not errs else "FAIL"}: {len(keys)} keys, {n_ent} entities/mapped, {len(errs)} errors')
sys.exit(1 if errs else 0)
