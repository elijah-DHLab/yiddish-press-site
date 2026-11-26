# -*- coding: utf-8 -*-
import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, 'kb/scripts')
from kblib import *
from build2 import E

rows = [l.split('\t') for l in open('kb/work/batch_ppl_2.tsv', encoding='utf-8').read().splitlines()[1:]]
KEY = {i: r[0] for i, r in enumerate(rows, 1)}
arts = {}
for l in open('kb/work/articles.jsonl', encoding='utf-8'):
    a = json.loads(l)
    for x in a['ppl']:
        arts.setdefault(norm_key(split_item(x)[0]), []).append((a['id'], a['d']))

RENAME = {'ppl:fyodor-trepov-1858': 'ppl:fyodor-fyodorovich-trepov'}
FIX_HE = {'ppl:eleftherios-venizelos': 'אלפתריוס ונייזלוס'}
DROP_IDS = {'ppl:mendelssohn-banker'}

ents = []
for d in E:
    if d['id'] in DROP_IDS: continue
    d['id'] = RENAME.get(d['id'], d['id'])
    if d['id'] in FIX_HE: d['he'] = FIX_HE[d['id']]
    out = {'id': d['id'], 'he': d['he'], 'en': d['en']}
    if d.get('en_alt'): out['en_alt'] = d['en_alt']
    out['desc'] = d['desc']
    if d.get('role'): out['role'] = d['role']
    out['kind'] = d['kind']
    if d.get('country'): out['country'] = d['country']
    if d.get('parent'): out['parent'] = d['parent']
    out['keys'] = [KEY[i] for i in d['keys']]
    ents.append(out)

def morocco(date):
    if date < '1908-08-23': return 'ppl:abdelaziz-of-morocco'
    if date < '1912-08-12': return 'ppl:abd-al-hafid'
    return 'ppl:yusef-of-morocco'

def ottoman(date):
    return 'ppl:abdul-hamid-ii' if date < '1909-04-27' else 'ppl:mehmed-v'

OTTOMAN_ARTS = {'dfr19050410-01.2.12', 'dfr19050521-01.2.7', 'unzerleben19090505-01.2.7'}
OTTOMAN_ARTS |= {aid for aid, d in arts['סולטאן'] if aid.startswith('unzerleben1908') or aid.startswith('unzerleben19090')}
OTTOMAN_ARTS |= {'unzerleben19100502-01.2.3', 'unzerleben19100821-01.2.3', 'unzerleben19110511-01.2.4',
                 'unzerleben19110516-01.2.3', 'unzerleben19110619-01.2.2'}

def sultan(aid, date):
    if aid in OTTOMAN_ARTS:
        return 'ppl:abdul-hamid-ii' if aid == 'unzerleben19090505-01.2.7' else ottoman(date)
    return morocco(date)

ctx_rules = {
    6: lambda a, d: 'ppl:vladimir-mikhailovich-volkonsky' if a in ('hyt19110405-01.2.7', 'hyt19110703-01.2.16') else None,
    30: lambda a, d: 'ppl:henry-lane-wilson' if d < '1912' else 'ppl:woodrow-wilson',
    62: lambda a, d: 'ppl:ivan-vasiliev-gapon-assembly' if d < '1906' else None,
    201: lambda a, d: 'ppl:grigori-trubetskoy' if d >= '1914' else None,
    218: lambda a, d: 'ppl:vladimir-trepov' if a == 'hyt19110427-01.2.3' else 'ppl:fyodor-fyodorovich-trepov',
    353: lambda a, d: 'ppl:levy-lisbon' if d < '1913' else 'ppl:levi-ben-nahshon',
    354: lambda a, d: 'ppl:levin-odessa-1905' if d < '1906' else None,
    458: lambda a, d: 'ppl:george-v' if d < '1911' else 'ppl:edward-viii',
    481: lambda a, d: None,
    543: lambda a, d: 'ppl:ernst-von-mendelssohn-bartholdy' if d < '1909' else None,
    581: lambda a, d: 'ppl:nikolai-maklakov' if a in ('unzerleben19130323-01.2.13', 'unzerleben19130507-01.2.2', 'unzerleben19140910-01.2.21') else 'ppl:vasily-maklakov',
    588: lambda a, d: None if d < '1907' else 'ppl:alexander-makarov',
    619: lambda a, d: 'ppl:frank-marshall' if d >= '1912' else None,
    672: lambda a, d: 'ppl:nicholas-i-of-montenegro' if d < '1909' else 'ppl:prince-nicholas-of-greece-and-denmark',
    731: sultan,
    736: lambda a, d: morocco(d),
    601: lambda a, d: morocco(d), 602: lambda a, d: morocco(d),
    603: lambda a, d: morocco(d), 604: lambda a, d: morocco(d),
}
ctx = []
for i, f in ctx_rules.items():
    k = KEY[i]
    ctx.append({'key': k, 'articles': {aid: f(aid, d) for aid, d in arts[k]}})

ids = {e['id'] for e in ents}
for c in ctx:
    for v in c['articles'].values():
        if v and v not in ids: print('MISSING TARGET', v)
drop = []
json.dump({'entities': ents, 'contextual': ctx, 'drop': drop}, open('kb/work/ent_ppl_2.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(ents), 'entities', len(ctx), 'contextual')
