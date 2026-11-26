import json,sys
sys.stdout.reconfigure(encoding='utf-8')
d=json.load(open('kb/work/ent_pl_1.json',encoding='utf-8'));c=json.load(open('kb/work/ent_pl_1.cand.json',encoding='utf-8'))
for e in d['entities']:
    cs=c.get(e['id'],[]);a=e.get('qid_auto')
    if not cs: continue
    if a and sum(1 for x in cs if x.get('name_match') and x.get('type_ok'))==1: continue
    print(f"{e['id']} [{e['desc'][:40]}] auto={a}")
    for x in cs[:6]:
        if not (x.get('type_ok') or x.get('name_match')): continue
        print(f"  {x['qid']} {x['en'][:30]}|{x.get('desc','')[:55]}|{x.get('sitelinks')}")
