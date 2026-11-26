#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_data.py — ממיר את גיליון הניתוח (xlsx או csv) ל-data.json שהאתר טוען,
ומקשר כל כתבה לישויות של מאגר הידע (kb/): אנשים, מקומות, ארגונים, קבוצות, נושאים ואירועים.

שימוש:
    python build_data.py analysis_an-002.xlsx [imgmap.json]

מאגר הידע (נבנה ע"י kb/scripts, ראו kb/README.md):
    kb/entities.json       הישויות (שם, תיאור, היררכיה, מזהה ויקידאטה)
    kb/surface_forms.json  כתיב בגיליון -> מזהי ישויות (+ זיהוי לפי הקשר בכתבה מסוימת)
    kb/relations.json      הקשרים בין הישויות (אונטולוגיה)
    kb/wikidata.json       ההעשרה מוויקידאטה
כתיב שאינו מוכר למאגר (שורות חדשות בגיליון) נשמר כישות זמנית "?:" ומדווח בסוף הריצה —
יש להריץ את kb/scripts כדי לשייך אותו.
"""
import sys, re, json, csv, collections, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'kb', 'scripts'))
from kblib import parse_list, norm_key, load_json, KB

SRC = sys.argv[1] if len(sys.argv) > 1 else 'analysis_an-002.xlsx'
IMG = sys.argv[2] if len(sys.argv) > 2 else 'imgmap.json'
OUT = 'data.json'
if hasattr(sys.stdout, 'reconfigure'): sys.stdout.reconfigure(encoding='utf-8')

# ---------- קריאה ----------
def read_rows(path):
    if path.lower().endswith('.csv'):
        with open(path, encoding='utf-8-sig', newline='') as f:
            return list(csv.reader(f))
    import openpyxl
    wb = openpyxl.load_workbook(path, read_only=True)
    return [list(r) for r in wb.worksheets[0].iter_rows(values_only=True)]

rows = read_rows(SRC)
hdr = [str(h or '').strip() for h in rows[0]]
col = {h: i for i, h in enumerate(hdr)}
def need(name):
    for h in col:
        if h.startswith(name): return col[h]
    raise SystemExit('חסרה עמודה: ' + name)
I = dict(id=need('מזהה'), paper=need('עיתון'), date=need('תאריך'), url=need('קישור'),
         terms=need('מילות חיפוש'), sum=need('סיכום'), ctx=need('מה נאמר'), cen=need('מרכזיות'),
         ppl=need('אנשים'), pl=need('מקומות'), org=need('ארגונים'), grp=need('קבוצות'),
         top=need('נושאים'), genre=need('סוגה'), rel=need('רלוונטיות'), ocr=need('טקסט ביידיש'))
imgmap = json.load(open(IMG, encoding='utf-8')) if os.path.exists(IMG) else {}

# ---------- מאגר הידע ----------
E = load_json(os.path.join(KB, 'entities.json'), {})
SFall = load_json(os.path.join(KB, 'surface_forms.json'), {'map': {}, 'contextual': {}, 'dropped': {}})
SF, CTX, DROP = SFall['map'], SFall['contextual'], SFall['dropped']
REL = load_json(os.path.join(KB, 'relations.json'), [])
W = load_json(os.path.join(KB, 'wikidata.json'), {})
RD = load_json(os.path.join(KB, 'redirects.json'), {})
SRC_TYPES = ('ppl', 'pl', 'org', 'grp', 'top')
OUT_TYPES = ('top', 'ev', 'ppl', 'pl', 'org', 'grp')
rd = lambda i: RD.get(i, i)
unknown = collections.Counter()

def resolve(t, h, aid):
    k = norm_key(h)
    if not k: return []
    c = CTX.get(t, {}).get(k)
    if c is not None and aid in c:
        return [rd(c[aid])] if c[aid] else []
    if k in SF.get(t, {}): return [rd(x) for x in SF[t][k]]
    if k in DROP.get(t, {}): return []
    unknown[(t, k)] += 1
    return ['?' + t + ':' + k]

# היררכיה: הורים של כל ישות (לחיפוש "כולל תתי-נושאים / מקומות בתוך")
UP_P = {'located_in', 'broader', 'part_of'}
up = collections.defaultdict(list)
for s, p, o, src in REL:
    if p in UP_P and s in E and o in E and o not in up[s]:
        # אצל מקומות: עדיפות להורה שנקבע במאגר; ויקידאטה רק אם אין
        if src == 'wikidata' and E[s]['type'] == 'pl' and E[s].get('parent'): continue
        up[s].append(o)
def ancestors(i):
    out, st = [], list(up.get(i, []))
    while st:
        x = st.pop()
        if x in out or x == i: continue
        out.append(x); st.extend(up.get(x, []))
    return out

# נושאי-על = מושגי השורש של אוצר המילים
top_roots = [e['id'] for e in E.values() if e['type'] == 'top' and not e.get('broader')]
vocab_order = {i: n for n, i in enumerate(e['id'] for e in E.values() if e['type'] == 'top')}
top_roots.sort(key=lambda i: vocab_order.get(i, 9999))
COUNTRY_KIND = re.compile(r'country|empire|kingdom|state|sultanate|protectorate|principality|republic|monarchy|emirate|khanate|grand duchy', re.I)
def is_country(i):
    e = E.get(i, {})
    return e.get('type') == 'pl' and (COUNTRY_KIND.search(e.get('kind', '') or '') is not None)
JEW_TOP = re.compile(r'יהוד|ציונ|עלילת|פוגרומ|קהיל|אנטישמ|ארץ ישראל|הגירה')
jew_grp = {i for i in E if i == 'grp:jews' or 'grp:jews' in ancestors(i)}

# ---------- בניית הרשומות ----------
arts = []
for r in rows[1:]:
    if not r or not r[I['id']]: continue
    g = lambda k: ('' if r[I[k]] is None else str(r[I[k]]).strip())
    aid = g('id')
    lists = {k: parse_list(g(k)) for k in SRC_TYPES}
    ids = {t: [] for t in OUT_TYPES}
    for t in SRC_TYPES:
        for h, y in lists[t]:
            for x in resolve(t, h, aid):
                tt = x.split(':')[0].lstrip('?')
                tt = tt if tt in ids else t
                if x not in ids[tt]: ids[tt].append(x)
    # נושאי-על, נושא ראשי, מדינות, הקשר יהודי
    tags = [x for x in ids['top'] + ids['ev'] if x in E]
    sc = collections.Counter()
    for x in tags:
        for rt in ([x] if x in top_roots else []) + [a for a in ancestors(x) if a in top_roots]:
            sc[rt] += 1
    th = [k for k in top_roots if k in sc] or ['other']
    pt = sorted(th, key=lambda k: (-sc[k], vocab_order.get(k, 9999)))[0] if sc else 'other'
    cn = []
    for x in ids['pl']:
        for y in [x] + ancestors(x):
            if is_country(y) and y not in cn: cn.append(y)
    alltags = set(x for t in ids for x in ids[t])
    jewish = bool(alltags & jew_grp) or any(JEW_TOP.search(E[y]['he']) for x in tags for y in [x] + ancestors(x) if y in E and E[y]['type'] == 'top')
    a = dict(id=aid, p=g('paper'), d=g('date'), u=g('url').replace('\\&', '&'),
             t=[x.strip() for x in g('terms').split(';') if x.strip()],
             s=g('sum'), c=g('ctx'), m=g('cen'), g=g('genre'), r=g('rel'),
             **ids, tr=[h for h, _ in lists['top']], th=th, pt=pt, cn=cn, jw=1 if jewish else 0,
             im=imgmap.get(aid, []), o=g('ocr'))
    arts.append(a)

arts.sort(key=lambda a: (a['d'], a['p'], a['id']))
for i, a in enumerate(arts): a['n'] = i

# ---------- ישויות לייצוא (רק אלה שבשימוש + אבותיהן) ----------
used = set()
for a in arts:
    for t in OUT_TYPES: used.update(a[t])
for a in arts: used.update(a['cn'])
for x in list(used): used.update(ancestors(x))
for s, p, o, src in REL:   # שכנים ישירים בגרף, כדי שקישורים בדף הישות יעבדו
    if s in used and o in E: used.add(o)
yid = collections.defaultdict(collections.Counter)
for r in rows[1:]:
    if not r or not r[I['id']]: continue
    aid = str(r[I['id']]).strip()
    for t in SRC_TYPES:
        for h, y in parse_list('' if r[I[t]] is None else str(r[I[t]])):
            if not y: continue
            for x in resolve(t, h, aid): yid[x][y] += 1

ents = {t: {} for t in OUT_TYPES}
for x in sorted(used):
    if x.startswith('?'):
        t, k = x[1:].split(':', 1)
        ents[t][x] = dict(h=k, y=[y for y, _ in yid[x].most_common(3)], un=1)
        continue
    e = E.get(x)
    if not e: continue
    w = W.get(e.get('qid') or '', {})
    o = dict(h=e['he'], y=[y for y, _ in yid[x].most_common(3)])
    if not o['y'] and w.get('yi'): o['y'] = [w['yi']]
    for src, dst in (('en', 'en'), ('kind', 'k'), ('role', 'ro'), ('scope', 'sc'), ('date', 'dt'), ('end', 'de'), ('qid', 'q')):
        if e.get(src): o[dst] = e[src]
    if w.get('dhe') or e.get('desc'): o['ds'] = w.get('dhe') or e.get('desc')
    for src, dst in (('lat', 'lat'), ('lon', 'lon'), ('born', 'b'), ('died', 'x'), ('start', 'st'), ('end', 'en_'), ('hew', 'wh'), ('enw', 'we'), ('yiw', 'wy'), ('img', 'img')):
        if w.get(src) not in (None, ''): o[dst] = w[src]
    al = [k for k in e.get('aliases', []) if k != e['he']]
    if w.get('he') and w['he'] != e['he']: al.append(w['he'])
    if al: o['a'] = sorted(set(al))
    if up.get(x): o['up'] = [u for u in up[x] if u in used]
    ents[e['type']][x] = o
for x in used:   # countries/ancestors referenced but typed elsewhere
    pass
rels = [[s, p, o] + ([1] if src == 'wikidata' else []) for s, p, o, src in REL if s in used and o in used]

themes = [dict(k=k, h=E[k]['he']) for k in top_roots] + [dict(k='other', h='אחר / לא מסווג')]
meta = dict(rows=len(arts), built=__import__('datetime').date.today().isoformat(), themes=themes,
            source=os.path.basename(SRC),
            kb=dict(entities=sum(len(v) for v in ents.values()), wikidata=sum(1 for t in ents.values() for o in t.values() if o.get('q')),
                    relations=len(rels), surface_forms=sum(len(v) for v in SF.values())))
ocr = {a['id']: a.pop('o') for a in arts}
json.dump(dict(meta=meta, ents=ents, rels=rels, arts=arts), open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
json.dump(ocr, open('ocr.json', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print('articles', len(arts), 'size KB', os.path.getsize(OUT) // 1024, ' ocr KB', os.path.getsize('ocr.json') // 1024)
print('entities exported', {t: len(v) for t, v in ents.items()}, ' relations', len(rels))
print('themes(any)', collections.Counter(t for a in arts for t in a['th']).most_common())
print('themes(primary)', collections.Counter(a['pt'] for a in arts).most_common())
print('jewish', sum(a['jw'] for a in arts), ' no-topic', sum(1 for a in arts if a['th'] == ['other']))
if unknown:
    print(f'!! {len(unknown)} surface forms unknown to the KB (run kb/scripts to resolve), e.g.:')
    for (t, k), n in unknown.most_common(15): print('   ', t, k, n)
