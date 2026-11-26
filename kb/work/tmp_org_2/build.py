# -*- coding: utf-8 -*-
import sys, os, json
sys.path.insert(0, 'kb/scripts')
from kblib import *
sys.stdout.reconfigure(encoding='utf-8')

BATCH = 'kb/work/batch_org_2.tsv'
keys = [l.split('\t')[0] for l in open(BATCH, encoding='utf-8').read().splitlines()[1:] if l.strip()]
keyset = set(keys)
arts = {}
for l in open('kb/work/articles.jsonl', encoding='utf-8'):
    a = json.loads(l)
    for x in a['org']:
        arts.setdefault(norm_key(split_item(x)[0]), []).append(a['id'])

def K(k):
    if k in keyset: return k
    c = [x for x in keys if x.startswith(k)]
    if len(c) == 1: return c[0]
    raise SystemExit(f'KEY? {k!r} -> {c}')

C = {'F': 'pl:france', 'R': 'pl:russian-empire', 'O': 'pl:ottoman-empire', 'G': 'pl:germany', 'UK': 'pl:united-kingdom',
     'A': 'pl:austria-hungary', 'I': 'pl:italy', 'S': 'pl:spain', 'US': 'pl:united-states', 'M': 'pl:morocco',
     'P': 'pl:persia', 'J': 'pl:japan', 'CN': 'pl:china', 'GR': 'pl:greece', 'BG': 'pl:bulgaria', 'SR': 'pl:serbia',
     'RO': 'pl:romania', 'MN': 'pl:montenegro', 'AL': 'pl:albania', 'EG': 'pl:egypt', 'PT': 'pl:portugal', 'NL': 'pl:netherlands',
     'CH': 'pl:switzerland', 'SE': 'pl:sweden', 'DK': 'pl:denmark', 'NO': 'pl:norway', 'PL': 'pl:poland', 'FI': 'pl:finland',
     'BE': 'pl:belgium', 'PAL': 'pl:ottoman-palestine', 'SY': 'pl:syria', 'CAU': 'pl:caucasus', 'MK': 'pl:macedonia',
     'AR': 'pl:argentina', 'AU': 'pl:australia', 'CA': 'pl:canada', 'MX': 'pl:mexico', 'HU': 'pl:austria-hungary', '': None}

ents = {}
order = []
def E(id, he, en, desc, kind, country='', keys='', parent=None, alt=None):
    ks = [K(k.strip()) for k in keys.split('|') if k.strip()] if keys else []
    if id in ents:
        ents[id]['keys'] += ks; return
    e = {'id': id, 'he': he, 'en': en}
    if alt: e['en_alt'] = alt
    e['desc'] = desc; e['kind'] = kind
    if parent: e['parent'] = parent
    cc = C.get(country, country) if country else None
    if cc: e['country'] = cc
    e['keys'] = ks
    ents[id] = e; order.append(id)

ctx = []
def X(key, default, over=None):
    k = K(key)
    m = {aid: default for aid in arts[k]}
    for aid, v in (over or {}).items():
        assert aid in m, (k, aid)
        m[aid] = v
    ctx.append({'key': k, 'articles': m})

drops = []
def D(key, why):
    drops.append({'key': K(key), 'why': why})

for f in ('data','data2','data3','data4','data5'): exec(open(f'kb/work/tmp_org_2/{f}.py', encoding='utf-8').read())

out = {'entities': [ents[i] for i in order], 'contextual': ctx, 'drop': drops}
used = set()
for e in out['entities']: used |= set(e['keys'])
for c in ctx: used.add(c['key'])
for d in drops: used.add(d['key'])
missing = [k for k in keys if k not in used]
print('missing', len(missing)); print(' | '.join(missing[:200]))
# dup check
from collections import Counter
cnt = Counter([k for e in out['entities'] for k in e['keys']] + [c['key'] for c in ctx] + [d['key'] for d in drops])
print('dups', [k for k, v in cnt.items() if v > 1])
# contextual targets defined?
ids = set(ents)
for c in ctx:
    for v in c['articles'].values():
        if v and v not in ids: print('undefined target', c['key'], v)
save_json('kb/work/ent_org_2.json', out)
print(len(out['entities']), len(ctx), len(drops))
