import sys,json
sys.stdout.reconfigure(encoding='utf-8')
ids=set(sys.argv[1:])
for l in open('kb/work/articles.jsonl',encoding='utf-8'):
    a=json.loads(l)
    if a['id'] in ids:
        print('##',a['id'],a['s'][:400],'|| C:',a.get('c','')[:300],'|| G:',a['grp'],'|| PL:',a['pl'][:10])
