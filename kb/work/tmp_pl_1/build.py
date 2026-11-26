import sys, json, os
sys.path.insert(0, 'kb/scripts')
from kblib import *
sys.stdout.reconfigure(encoding='utf-8')
rows = [l.split('\t') for l in open('kb/work/batch_pl_1.tsv', encoding='utf-8').read().splitlines()[1:] if l.strip()]
keys = [r[0] for r in rows]
K = lambda n: keys[int(n) - 1]
used = {}
ents = []
for line in open('kb/work/tmp_pl_1/ents.txt', encoding='utf-8'):
    line = line.rstrip('\n')
    if not line.strip(): continue
    i, he, en, desc, kind, parent, nums = line.split('|')
    ks = [K(n) for n in nums.split(',') if n.strip()]
    for n in nums.split(','):
        if n.strip():
            if n in used: print('DUP', n, i, used[n])
            used[n] = i
    e = {'id': i, 'he': he, 'en': en, 'desc': desc, 'kind': kind}
    if parent: e['parent'] = parent
    e['keys'] = ks
    ents.append(e)

drops = {11: 'unidentifiable OCR form', 23: 'unidentifiable OCR form', 37: 'means "abroad", not a place name',
         39: 'unidentifiable OCR form', 61: 'unidentifiable OCR form', 74: 'generic "vilayet" (province)',
         110: 'unidentifiable OCR form', 137: 'unidentifiable OCR form', 174: 'unidentifiable OCR form',
         191: 'garbled extractor label, unidentifiable', 199: 'unidentifiable OCR form', 262: 'generic "Jewish cemetery"',
         317: 'generic border reference', 318: 'generic border reference', 319: 'generic border reference', 320: 'generic border reference',
         342: '"hell", metaphorical', 409: 'generic direction, not a place', 433: 'unidentifiable OCR form',
         481: 'unidentifiable OCR form', 489: 'unidentifiable OCR form', 512: 'unidentifiable OCR form',
         524: 'means "abroad", not a place name', 550: 'unidentifiable (historical fiction)', 579: 'unidentifiable OCR form'}
for n in drops:
    if str(n) in used: print('drop also used', n)
arts = {}
for l in open('kb/work/articles.jsonl', encoding='utf-8'):
    a = json.loads(l)
    for x in a['pl']:
        arts.setdefault(norm_key(split_item(x)[0]), set()).add(a['id'])
ctx = []
def cmap(n, f):
    k = K(n)
    ctx.append({'key': k, 'articles': {a: f(a) for a in sorted(arts.get(k, []))}})
cmap(183, lambda a: 'pl:aram' if a.startswith('unzerleben19150126') else None)
cmap(308, lambda a: 'pl:brest-belarus' if a.startswith('dfr1907') else 'pl:brest-france')
cmap(607, lambda a: 'pl:tripoli-libya')
ctxn = {183, 308, 607}
allused = set(int(n) for n in used) | set(drops) | ctxn
missing = [i for i in range(1, len(keys) + 1) if i not in allused]
print('missing', [(i, keys[i-1]) for i in missing])
out = {'entities': ents, 'contextual': ctx, 'drop': [{'key': K(n), 'why': w} for n, w in sorted(drops.items())]}
json.dump(out, open('kb/work/ent_pl_1.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(ents), len(ctx), len(drops))
