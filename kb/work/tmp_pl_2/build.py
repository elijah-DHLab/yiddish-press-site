import json,csv,sys,re
sys.stdout.reconfigure(encoding='utf-8')
rows=list(csv.DictReader(open('kb/work/batch_pl_2.tsv',encoding='utf-8'),delimiter='\t'))
disp={r['key']:r['display'] for r in rows}
yid={r['key']:r['yiddish'] for r in rows}
ents={}
def E(id,he,en,desc,kind,parent,keys,alt=None,**kw):
    if isinstance(keys,str): keys=[k.strip() for k in keys.split(';') if k.strip()]
    if id in ents:
        ents[id]['keys']+=keys; return
    e={'id':id,'he':he,'en':en}
    if alt: e['en_alt']=alt
    e.update({'desc':desc,'kind':kind})
    if parent: e['parent']=parent
    e.update(kw)
    e['keys']=keys
    ents[id]=e
def U(id,key,parent,where,kind='place'):
    """unidentified place"""
    y=yid.get(key,'').split(' | ')[0]
    E(id,disp.get(key,key),id.split(':')[1].replace('-',' ').title(),
      f"unidentified {kind} in {where} (Yiddish: {y})" if y else f"unidentified {kind} in {where}",kind,parent,[key])
exec(open('kb/work/tmp_pl_2/data.py',encoding='utf-8').read())
out={'entities':list(ents.values()),'contextual':CTX,'drop':DROP}
json.dump(out,open('kb/work/ent_pl_2.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(len(ents),'entities')
