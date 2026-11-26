import sys, json
sys.path.insert(0, 'kb/scripts')
from kblib import *
sys.stdout.reconfigure(encoding='utf-8')
arts = {}
for l in open('kb/work/articles.jsonl', encoding='utf-8'):
    a = json.loads(l); arts[a['id']] = a
rows = {l.split('\t')[0]: l.rstrip('\n').split('\t') for l in open('kb/work/batch_ppl_3.tsv', encoding='utf-8')}
W = int(sys.argv[1])
for key in sys.argv[2:]:
    r = rows[key]; print('##', key)
    for aid in r[7].split():
        a = arts[aid]
        ent = [x for x in a['ppl'] if norm_key(split_item(x)[0]) == key]
        oth = [split_item(x)[0] for x in a['ppl'] if norm_key(split_item(x)[0]) != key][:5]
        print(f"  {aid} {a['d']} | {ent[0] if ent else ''} | {a['s'][:W]} | co: {', '.join(oth)}")
