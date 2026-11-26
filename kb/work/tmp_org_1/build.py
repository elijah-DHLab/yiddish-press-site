# -*- coding: utf-8 -*-
import json, sys, os
sys.path.insert(0, 'kb/scripts')
from kblib import *
sys.stdout.reconfigure(encoding='utf-8')

rows = [l.rstrip('\n').split('\t') for l in open('kb/work/batch_org_1.tsv', encoding='utf-8').read().splitlines()[1:] if l.strip()]
KEYS = [r[0] for r in rows]
ARTS = {k: [] for k in KEYS}
for l in open('kb/work/articles.jsonl', encoding='utf-8'):
    a = json.loads(l)
    for x in a['org']:
        kk = norm_key(split_item(x)[0])
        if kk in ARTS and a['id'] not in ARTS[kk]: ARTS[kk].append(a['id'])
def K(spec):
    out = []
    for part in str(spec).split(','):
        part = part.strip()
        if not part: continue
        if '-' in part:
            a, b = part.split('-'); out += [KEYS[i - 1] for i in range(int(a), int(b) + 1)]
        else: out.append(KEYS[int(part) - 1])
    return out

RU, FR, DE, OT, UK, AT, IT, US = 'pl:russian-empire', 'pl:france', 'pl:germany', 'pl:ottoman-empire', 'pl:united-kingdom', 'pl:austria-hungary', 'pl:italy', 'pl:united-states'
ents = []
def E(id, he, en, desc, kind, idx='', country=None, parent=None, alt=None):
    e = {'id': id, 'he': he, 'en': en}
    if alt: e['en_alt'] = alt
    e['desc'] = desc; e['kind'] = kind
    if parent: e['parent'] = parent
    if country: e['country'] = country
    e['keys'] = K(idx) if idx else []
    ents.append(e)

ctx = []
def C(i, mapping):
    """mapping: dict article->id, or a single id/None applied to all articles"""
    k = KEYS[i - 1]
    arts = ARTS[k]
    if not isinstance(mapping, dict): mapping = {a: mapping for a in arts}
    else:
        m2 = {}
        for a in arts:
            m2[a] = mapping.get(a, mapping.get(a[:13], None)) if a not in mapping else mapping[a]
        mapping = m2
    ctx.append({'key': k, 'articles': mapping})

drops = []
def D(idx, why):
    for k in K(idx): drops.append({'key': k, 'why': why})

exec(open('kb/work/tmp_org_1/data.py', encoding='utf-8').read())

# sanity
used = {}
for e in ents:
    for k in e['keys']: used.setdefault(k, []).append(e['id'])
for c in ctx: used.setdefault(c['key'], []).append('ctx')
for d in drops: used.setdefault(d['key'], []).append('drop')
dups = {k: v for k, v in used.items() if len(v) > 1}
if dups: print('DUP', dups)
miss = [ (i+1, k) for i, k in enumerate(KEYS) if k not in used]
if miss: print('MISSING', miss)
ids = [e['id'] for e in ents]
import collections
for i, n in collections.Counter(ids).items():
    if n > 1: print('DUPID', i)
allids = set(ids)
for c in ctx:
    for v in c['articles'].values():
        if v and v not in allids: print('ctx target missing', c['key'], v)
json.dump({'entities': ents, 'contextual': ctx, 'drop': drops}, open('kb/work/ent_org_1.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(ents), 'entities', len(ctx), 'ctx', len(drops), 'drops')
