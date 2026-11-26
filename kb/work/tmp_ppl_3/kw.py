import sys, json, re
sys.path.insert(0, 'kb/scripts')
from kblib import *
sys.stdout.reconfigure(encoding='utf-8')
arts = {}
for l in open('kb/work/articles.jsonl', encoding='utf-8'):
    a = json.loads(l); arts[a['id']] = a
rows = {l.split('\t')[0]: l.rstrip('\n').split('\t') for l in open('kb/work/batch_ppl_3.tsv', encoding='utf-8')}
key = sys.argv[1]; pats = sys.argv[2:]
for aid in rows[key][7].split():
    a = arts[aid]; txt = a['s'] + ' || ' + a.get('c', '')
    hits = []
    for p in pats:
        for m in re.finditer(p, txt):
            hits.append(txt[max(0, m.start()-120): m.end()+120])
    print(f"== {aid} {a['d']} :: " + (' ### '.join(hits) if hits else a['s'][:200]))
