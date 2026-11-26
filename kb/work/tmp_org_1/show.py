import sys, os, json
sys.path.insert(0, 'kb/scripts')
from kblib import *
sys.stdout.reconfigure(encoding='utf-8')
arts = {}
for l in open('kb/work/articles.jsonl', encoding='utf-8'):
    a = json.loads(l); arts[a['id']] = a
rows = {l.split('\t')[0]: l.rstrip('\n').split('\t') for l in open('kb/work/mentions_org.tsv', encoding='utf-8')}
n = int(os.environ.get('N', '170'))
for k in open(sys.argv[1], encoding='utf-8').read().splitlines():
    k = k.strip()
    if not k: continue
    r = rows.get(k)
    if not r: print('?? missing', k); continue
    print(f'### {k} [{r[3][:60]}]')
    for aid in r[7].split(' '):
        if not aid: continue
        a = arts[aid]
        orgs = [x for x in a['org'] if norm_key(split_item(x)[0]) == k]
        print(f"  {aid} {a['d']} {a['s'][:n]}")
