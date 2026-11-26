import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')
W = os.path.join(os.path.dirname(__file__), '..')
keys = [l.rstrip('\n').split('\t') for l in open(os.path.join(W, 'tbatch_3.tsv'), encoding='utf-8')][1:]
vocab = json.load(open(os.path.join(W, 'vocab.json'), encoding='utf-8'))
txt = json.dumps(vocab, ensure_ascii=False)
m = {}
for l in open(os.path.join(os.path.dirname(__file__), 'm1.txt'), encoding='utf-8'):
    p = l.split()
    if not p: continue
    ids = [x if ':' in x else 'top:' + x for x in p[1:]]
    for i in ids:
        assert '"%s"' % i in txt, i
    m[int(p[0])] = ids
assert sorted(m) == list(range(1, len(keys) + 1)), (len(m), len(keys))
out = {k[0]: m[i + 1] for i, k in enumerate(keys)}
suggest = [
    {"key": "פוגרום נגד שחורים בארצות הברית", "note": "racial violence / lynching in the US (no race-relations concept; mapped to americas-politics)"},
    {"key": "פרשת איליודור", "note": "Russian Orthodox Church / clergy affairs (Iliodor) - no concept for Orthodox church; mapped to russian-government"},
    {"key": "קונגרס בינלאומי של כבאים", "note": "international (non-political) congresses and associations; mapped to fires"},
    {"key": "קשר בין יהודים למלחמה ושלום", "note": "antisemitic linking of Jews to war/finance (fits antisemitism, but maybe a 'Jews and international politics' concept)"},
    {"key": "שליוואַוויץ", "note": "kashrut/Passover product certification - covered by jewish-religious-life; fine"},
]
json.dump({"map": out, "suggest": suggest}, open(os.path.join(W, 'topicmap_3.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
if '--show' in sys.argv:
    for i, k in enumerate(keys):
        print(i + 1, k[0], k[2][:7], ' '.join(m[i + 1]))
