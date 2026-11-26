import csv, json, sys, collections, os
sys.stdout.reconfigure(encoding='utf-8')
W = 'kb/work/'
rows = list(csv.reader(open(W + 'tbatch_2.tsv', encoding='utf-8'), delimiter='\t', quoting=csv.QUOTE_NONE))[1:]
keys = [r[0] for r in rows if r and r[0].strip()]
vocab = json.load(open(W + 'vocab.json', encoding='utf-8'))
vids = {c['id'] for c in vocab['concepts']} | {e['id'] for e in vocab['events']}
m = {}
for f in ('m1.txt', 'm2.txt', 'm3.txt'):
    for line in open(W + 'tmp_tmap_2/' + f, encoding='utf-8'):
        p = line.split()
        if not p: continue
        i = int(p[0])
        ids = [x if ':' in x else 'top:' + x for x in p[1:]]
        for x in ids:
            if x not in vids: print('BAD', i, x)
        assert i not in m, i
        m[i] = ids
missing = [i for i in range(len(keys)) if i not in m]
print('keys', len(keys), 'mapped', len(m), 'missing', missing)
suggest = [
    {"key": keys[320], "note": "No concept for Romanian (and Balkan non-Ottoman) Jewry; consider 'יהדות רומניה והבלקן' under jewish-communities (also fits 'סיוע קהילתי ביהודי רומניה', 'מצב היהודים בסרביה')."},
    {"key": keys[720], "note": "No concept for Jewish demography/statistics (population counts, education statistics); mapped to jewish-communities."},
    {"key": keys[53], "note": "1915 references to a 'Jewish legion' (Zion Mule Corps) predate ev:jewish-legion (1917); mapped to wwi-jews only. Consider an event for the Zion Mule Corps or widening ev:jewish-legion."},
    {"key": keys[54], "note": "Polish legions / Polish question in WWI has no concept; mapped to wwi-eastern-front."},
    {"key": keys[626], "note": "No dedicated concept for Ottoman–Persian border dispute; such strings mapped to ottoman-foreign-relations."},
]
out = {"map": {keys[i]: m[i] for i in range(len(keys)) if i in m}, "suggest": suggest}
json.dump(out, open(W + 'topicmap_2.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
c = collections.Counter(x for v in out['map'].values() for x in v)
print(c.most_common(20))
