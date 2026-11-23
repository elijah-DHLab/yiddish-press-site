#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_data.py — ממיר את גיליון הניתוח (xlsx או csv) ל-data.json שהאתר טוען.

שימוש:
    python build_data.py analysis_an-002.xlsx            # → data.json
    python build_data.py analysis_an-002.csv  [imgmap.json]

imgmap.json (אופציונלי): מילון {מזהה-כתבה: [מזהי קבצי תמונה בגוגל דרייב]}
כשהגיליון גדל — מריצים שוב ומעלים את data.json החדש ל-GitHub.
"""
import sys, re, json, csv, collections, os

SRC = sys.argv[1] if len(sys.argv) > 1 else 'analysis_an-002.xlsx'
IMG = sys.argv[2] if len(sys.argv) > 2 else 'imgmap.json'
OUT = 'data.json'

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

# ---------- פירוק רשימות "עברית (יידיש) ; ..." ----------
def split_item(s):
    s = s.strip()
    if not s: return None
    if s.endswith(')'):
        depth = 0
        for i in range(len(s) - 1, -1, -1):
            if s[i] == ')': depth += 1
            elif s[i] == '(':
                depth -= 1
                if depth == 0:
                    h, y = s[:i].strip(), s[i + 1:-1].strip()
                    if h: return [h, y]
                    return [y, '']
    return [s, '']

def parse_list(v):
    if not v: return []
    out, seen = [], set()
    for part in re.split(r'\s*;\s*', str(v)):
        it = split_item(part)
        if it and it[0] not in seen:
            seen.add(it[0]); out.append(it)
    return out

def norm_key(h):
    h = re.sub(r'[\u05f3\u05f4"\'`’‘“”]', '', h)
    h = h.replace('־', ' ').replace('-', ' ')
    h = re.sub(r'\s+', ' ', h).strip()
    if len(h) > 3 and h[0] == 'ה': h = h[1:]
    return h

# ---------- נושאי-על (קיבוץ אוטומטי לפי מילות מפתח בשדה "נושאים") ----------
THEMES = [
 ('ww1',      'מלחמת העולם הראשונה', r"מלחמת העולם|המלחמה העולמית|פליטי מלחמה|חזית|מצור על|פלישה לבלגיה|גיוס"),
 ('balkan',   'מלחמות הבלקן והמלחמה האיטלקית־טורקית', r"בלקן|איטלקית|טריפולי|לוב\b|אלבני|מקדוניה|מונטנגרו|סרביה|בולגריה|כרתים|שאלת המזרח"),
 ('antijew',  'פוגרומים, עלילות דם והגבלות על יהודים', r"עלילת דם|עלילות דם|פוגרומ|פרעות|הגבלות|אנטישמ|בייליס|בילי?ס|גזירות|גירוש|תחום המושב|הגירה|סכנה ליהוד|רדיפ"),
 ('zion',     'ציונות וארץ ישראל', r"ציונ|ארץ.ישראל|פלשתינ|היישוב|הקונגרס הציוני|עלייה|עליה|חלוצ|תל.אביב|טריטוריאליזם|הקרן הקיימת|בצלאל"),
 ('eastjews', 'קהילות יהודיות ספרדיות ומזרחיות', r"ספרדי|סלוניקי|דמשק|יהודי המזרח|יהודי מרוקו|יהודי פרס|יהודי תימן|יהודי ארצות|יהודי בוכרה|מלאח|כל ישראל חברים|אליאנס|יהודי טורקיה|יהודי איראן"),
 ('morocco',  'מרוקו והמשברים המרוקאיים', r"מרוק|אלג.?סיראס|אגאדיר|אגדיר|קזבלנקה|מולאי|עבד אל|חפיד|מראכש|מרקש|טנג.ר|פאס\b|שאלת מרוקו"),
 ('ottoman',  'האימפריה העות׳מאנית והתורכים הצעירים', r"עות.מאנ|טורקי|תורכי|תורכיה|קושטא|סולטאן|חוקה בתורכיה|ועד ואיחוד|התורכים הצעירים|המהפכה התורכית|מהפכה בטורקיה"),
 ('russia',   'רוסיה: דומא, מהפכה ושלטון', r"דומ[הא]|סטוליפין|מהפכה ברוסיה|מהפכת 1905|פטרבורג|צאר|קוקובצוב|פורישקביץ|גוצ.קוב|מועצת המדינה|רוסית.יפנית|פורטסמות|ממשלת רוסיה|מדיניות רוסיה|פנים ברוסיה|רוסיה"),
 ('diplomacy','דיפלומטיה ויחסי מעצמות', r"דיפלומטי|ברית|הסכמ|אמנה|ועידה|יריבות|מעצמות|משבר בינלאומי|יחסי |שגריר|אנטנט|מדיניות חוץ|מדיניות בריטניה|מדיניות גרמניה|מדיניות צרפת"),
 ('religion', 'דת, רבנות וכנסייה', r"רבנ|כנסי|בית כנסת|כמורה|אפיפיור|ותיקן|שחיטה|מיסיונ|הלכה|רבנות"),
 ('culture',  'עברית, חינוך, ספרות ותרבות', r"עברית|חינוך|בית ספר|בתי ספר|ספרות|תרבות|תיאטרון|עיתונות|יידיש|אידיש|אוניברסיט|הוראה|מוסיקה|אמנות|מדע|שפה"),
 ('economy',  'כלכלה, מסחר ותחבורה', r"כלכל|מסחר|סחר|רכבת|בנק|מיסים|תעשיי|חקלאות|נמל|מטבע|הלוואה|בורסה|תחבורה|מלווה"),
 ('disaster', 'בריאות, אסונות ומגפות', r"כולרה|מגפ|רעידת|שריפה|אסון|הצפה|בריאות|רעב|טביעה|מחלה"),
]
# סדר הרשימה = עדיפות בשוויון ניקוד, בבחירת "נושא ראשי"
THEME_RX = [(k, re.compile(rx)) for k, _, rx in THEMES]
JEWISH_TOP = re.compile(r"יהוד|עלילת דם|פוגרומ|ציונ|בייליס|קהיל|כל ישראל|רבנ|ארץ.ישראל|ספרדי|בית כנסת|גירוש|פוגרומ")

def theme_scores(topic_strings, date=''):
    sc = collections.Counter()
    for t in topic_strings:
        for k, rx in THEME_RX:
            if k == 'ww1' and date < '1914-07-28': continue  # נושא זה מתויג רק מפרוץ המלחמה
            if rx.search(t): sc[k] += 1
    return sc

def themes_for(topic_strings, summary='', date=''):
    sc = theme_scores(topic_strings, date)
    if not sc and summary:
        sc = theme_scores([summary], date)
        sc = collections.Counter({k: 1 for k in list(sc)[:2]})  # גיבוי מצומצם לפי הסיכום
    if not sc: return ['other'], 'other'
    order = [k for k, _ in THEME_RX]
    allt = [k for k in order if k in sc]
    primary = sorted(allt, key=lambda k: (-sc[k], order.index(k)))[0]
    return allt, primary

# ---------- בניית הרשומות ----------
arts = []
for r in rows[1:]:
    if not r or not r[I['id']]: continue
    g = lambda k: ('' if r[I[k]] is None else str(r[I[k]]).strip())
    aid = g('id')
    lists = {k: parse_list(g(k)) for k in ('ppl', 'pl', 'org', 'grp', 'top')}
    ttxt = ' ; '.join(h for h, _ in lists['top'])
    th, pt = themes_for([h for h, _ in lists['top']], g('sum'), g('date'))
    gtxt = ' '.join(h for h, _ in lists['grp'])
    jewish = bool(re.search(r'יהוד', gtxt)) or bool(JEWISH_TOP.search(ttxt)) or ('antijew' in th) or ('zion' in th) or ('eastjews' in th)
    a = dict(id=aid, p=g('paper'), d=g('date'), u=g('url').replace('\\&', '&'),
             t=[x.strip() for x in g('terms').split(';') if x.strip()],
             s=g('sum'), c=g('ctx'), m=g('cen'), g=g('genre'), r=g('rel'),
             ppl=lists['ppl'], pl=lists['pl'], org=lists['org'], grp=lists['grp'], top=lists['top'],
             th=th, pt=pt, jw=1 if jewish else 0,
             im=imgmap.get(aid, []), o=g('ocr'))
    arts.append(a)

arts.sort(key=lambda a: (a['d'], a['p'], a['id']))
for i, a in enumerate(arts): a['n'] = i

# ---------- מפתחות ישויות (איחוד כתיבים) ----------
def add_keys(a):
    for typ in ('ppl', 'pl', 'org', 'grp', 'top'):
        keys, seen = [], set()
        for h, y in a[typ]:
            k = norm_key(h)
            if k and k not in seen: seen.add(k); keys.append(k)
        a['k_' + typ] = keys
for a in arts: add_keys(a)

# שם תצוגה ויידיש לכל מפתח: הנפוץ ביותר
disp = {t: collections.defaultdict(collections.Counter) for t in ('ppl', 'pl', 'org', 'grp', 'top')}
yid = {t: collections.defaultdict(collections.Counter) for t in ('ppl', 'pl', 'org', 'grp', 'top')}
for a in arts:
    for t in disp:
        for h, y in a[t]:
            k = norm_key(h)
            disp[t][k][h] += 1
            if y: yid[t][k][y] += 1
ents = {}
for t in disp:
    ents[t] = {k: dict(h=c.most_common(1)[0][0],
                       y=[y for y, _ in yid[t][k].most_common(3)])
               for k, c in disp[t].items()}

meta = dict(rows=len(arts), built=__import__('datetime').date.today().isoformat(),
            themes=[dict(k=k, h=h) for k, h, _ in THEMES] + [dict(k='other', h='אחר / כללי')],
            theme_rules={k: rx for k, _, rx in THEMES}, source=os.path.basename(SRC))
ocr = {a['id']: a.pop('o') for a in arts}
for a in arts:
    for t in ('ppl', 'pl', 'org', 'grp', 'top'): a.pop('k_' + t, None)
json.dump(dict(meta=meta, ents=ents, arts=arts), open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
json.dump(ocr, open('ocr.json', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print('ocr KB', os.path.getsize('ocr.json') // 1024)
print('articles', len(arts), 'size KB', os.path.getsize(OUT) // 1024)
print('themes(any)', collections.Counter(t for a in arts for t in a['th']).most_common())
print('themes(primary)', collections.Counter(a['pt'] for a in arts).most_common())
print('other-only', sum(1 for a in arts if a['th'] == ['other']), 'jewish', sum(a['jw'] for a in arts))
print({t: len(v) for t, v in ents.items()})
