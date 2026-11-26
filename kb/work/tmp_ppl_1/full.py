import sys, json
sys.path.insert(0, 'kb/scripts')
from kblib import *
sys.stdout.reconfigure(encoding='utf-8')
arts = [json.loads(l) for l in open('kb/work/articles.jsonl', encoding='utf-8')]
rows = [l.split('\t') for l in open('kb/work/batch_ppl_1.tsv', encoding='utf-8').read().splitlines()[1:]]
nums = [int(x) for x in sys.argv[1].split(',')]
for n in nums:
    key = rows[n-1][0]
    print(f'## {n} {key}')
    for a in arts:
        if any(norm_key(split_item(x)[0]) == key for x in a['ppl']):
            print(f"  {a['id']} {a['d']}: {a['s'][:600]} || C: {a.get('c','')[:300]}")
