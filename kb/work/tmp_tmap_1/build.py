import json, sys
sys.stdout.reconfigure(encoding='utf-8')
voc = json.load(open('kb/work/vocab.json', encoding='utf-8'))
ids = set()
def walk(o):
    if isinstance(o, dict):
        if 'id' in o and isinstance(o['id'], str): ids.add(o['id'])
        for v in o.values(): walk(v)
    elif isinstance(o, list):
        for v in o: walk(v)
walk(voc)
keys = [l.split('\t')[0] for l in open('kb/work/tbatch_1.tsv', encoding='utf-8').read().splitlines()[1:]]
m = {}
for l in open('kb/work/tmp_tmap_1/m1.txt', encoding='utf-8'):
    l = l.rstrip('\n')
    if not l: continue
    k, v = l.split('|')
    if k in m: print('DUP', k)
    m[k] = [x.replace('T:', 'top:', 1).replace('E:', 'ev:', 1) for x in v.split()]
for k, v in m.items():
    for x in v:
        if x not in ids: print('BADID', k, x)
miss = [k for k in keys if k not in m]; extra = [k for k in m if k not in keys]
print('missing', len(miss), miss[:50]); print('extra', len(extra), extra[:50])
suggest = [
 {"key": "גניבה בעומר מסגד בירושלים", "note": "Parker expedition / Temple Mount excavation scandal in Jerusalem (April 1911) – candidate event under ottoman-palestine or science-archaeology"},
 {"key": "חשד לגניבת אוצרות מסגד בירושלים", "note": "same as above: Parker expedition affair 1911"},
 {"key": "וצאה להורג של דרוזים בדמשק", "note": "1911 executions follow the 1910 Hauran Druze revolt (Sami Pasha), not the 1909 one; ev:hauran-druze-rebellion date (1909-05) should be checked / a 1910 event added"},
 {"key": "ביקור הסולטאן בסלוניקי", "note": "Mehmed V's Rumelia journey (June 1911: Salonica, Skopje, Kosovo) – recurrent in corpus, candidate event under ottoman-politics"},
 {"key": "חרם כלכלי נגד יוון", "note": "Ottoman boycott of Greek goods 1909–1911 (Cretan question) – candidate event, analogous to ev:ottoman-boycott-austria-1908"},
 {"key": "ארגון הצבאי והמלוכה", "note": "Greek political crisis 1910 (Military League vs. crown, Venizelos' arrival) – only ev:goudi-coup (1909) exists"},
 {"key": "גיוס כפוי לצבא העותמאני", "note": "no concept for the Ottoman home front / Ottoman Jews under WWI conscription and deportation apart from wwi-jews and wwi-home-front"},
 {"key": "חזית הקווקזית", "note": "pre-Sarikamish Caucasus fighting (Nov–Dec 1914) has no event; concept wwi-ottoman-fronts used"},
 {"key": "דו קרב ועיתונאות", "note": "duels/honour affairs (Suvorin duel 1912, others) have no concept; mapped to press-opinion-polemics"},
 {"key": "גל חום באירופה", "note": "1911 European heat wave & drought – recurrent in 1911 telegrams; could be an event under natural-disasters"},
]
json.dump({"map": m, "suggest": suggest}, open('kb/work/topicmap_1.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
from collections import Counter
c = Counter(x for v in m.values() for x in v)
print(len(m)); print(c.most_common(20))
