import sys, json, re, collections, os
sys.path.insert(0, 'kb/scripts'); sys.path.insert(0, 'kb/work/tmp_ppl_1')
from kblib import *
sys.stdout.reconfigure(encoding='utf-8')
from data4 import E, O, DROP
rows = [l.split('\t') for l in open('kb/work/batch_ppl_1.tsv', encoding='utf-8').read().splitlines()[1:]]
K = lambda n: rows[n-1][0]
arts = [json.loads(l) for l in open('kb/work/articles.jsonl', encoding='utf-8')]
def arts_of(key): return [(a['id'], a['d']) for a in arts if any(norm_key(split_item(x)[0]) == key for x in a['ppl'])]
ents = []
for x in E:
    d = {k: v for k, v in x.items() if k not in ('nums',) and v is not None}
    d['keys'] = [K(n) for n in x['nums']]
    ents.append(d)
for x in O:
    he = x['he'] or re.sub(r'\s*\(.*?\)\s*', ' ', K(x['nums'][0])).strip()
    d = dict(id='ppl:' + x['slug'], he=he, en=x['en'], desc=x['desc'], kind=x['kind'])
    if x['country']: d['country'] = x['country']
    d['keys'] = [K(n) for n in x['nums']]
    ents.append(d)
for d in ents:
    if d['id'].startswith('ppl:bleichroder'): d['id'] = 'org:s-bleichroder'
def ctx(n, f):
    return dict(key=K(n), articles={aid: f(aid, dt) for aid, dt in arts_of(K(n))})
contextual = [
    ctx(42, lambda a, d: 'ppl:victor-adler' if a == 'dfr19070823-01.2.1' else None),
    ctx(115, lambda a, d: None),
    ctx(131, lambda a, d: None),
    ctx(132, lambda a, d: 'ppl:grigory-alexinsky' if d.startswith('1907') else None),
    ctx(133, lambda a, d: None),
    ctx(475, lambda a, d: None),
    ctx(504, lambda a, d: None),
    ctx(606, lambda a, d: 'ppl:alfred-dreyfus' if a.startswith('dfr1907') else None),
    ctx(692, lambda a, d: 'ppl:abdelaziz-of-morocco' if d < '1908-08-20' else ('ppl:abd-al-hafid' if d < '1912-08-13' else 'ppl:yusef-of-morocco')),
]
drop = [dict(key=K(n), why=w) for n, w in DROP.items()]
cov = collections.Counter([k for d in ents for k in d['keys']] + [c['key'] for c in contextual] + [d['key'] for d in drop])
print('dup keys', [k for k in cov if cov[k] > 1])
miss = [f'{i}:{r[0]}' for i, r in enumerate(rows, 1) if r[0] not in cov]
print('missing', len(miss), ' '.join(miss))
ids = collections.Counter(d['id'] for d in ents); print('dup ids', [i for i in ids if ids[i] > 1])
json.dump(dict(entities=ents, contextual=contextual, drop=drop), open('kb/work/ent_ppl_1.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(ents), 'entities', len(contextual), 'ctx', len(drop), 'drop')
