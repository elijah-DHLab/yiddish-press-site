'use strict';
/* ====== כלי עזר, נרמול, אינדקסים וסינון ====== */
const H = { A: [], byId: new Map(), ents: {}, idx: {}, meta: null, ocr: null, ocrN: null };
const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const ltr = s => `<bdi dir="ltr">${s}</bdi>`;
const nf = n => Number(n).toLocaleString('he-IL');
const pct = (a, b) => b ? Math.round(1000 * a / b) / 10 : 0;

/* ====== הגדרות (אפשר לערוך) ====== */
H.PAPERS = {
  dfr:        { he: 'דער פריינד',   en: 'Der Fraynd', color: '#b4532a' },
  hyt:        { he: 'היינט',        en: 'Haynt',      color: '#1b6ca8' },
  unzerleben: { he: 'אונזר לעבן',   en: 'Unzer Leben', color: '#2f7d5b' }
};
H.TYPES = { top: 'נושאים', ev: 'אירועים', ppl: 'אנשים', pl: 'מקומות', org: 'ארגונים', grp: 'קבוצות אוכלוסייה' };
H.TYPE1 = { top: 'נושא', ev: 'אירוע', ppl: 'אדם', pl: 'מקום', org: 'ארגון', grp: 'קבוצה' };
/* שמות הקשרים באונטולוגיה: [יוצא, נכנס] */
H.PRED = {
  located_in: ['נמצא ב', 'מקומות בתוכו'], broader: ['תת־נושא / תת־קבוצה של', 'תתי־נושאים ותתי־קבוצות'], part_of: ['חלק מ', 'חלקים'],
  country: ['מדינה', 'קשורים למדינה'], related: ['קשור ל', 'קשורים אליו'], location: ['מקום האירוע', 'אירועים במקום'],
  participant: ['משתתפים', 'השתתף ב'], member_of: ['חבר ב', 'חברים']
};
H.CEN = ['נושא הכתבה', 'ידיעה אחת מתוך כמה', 'אזכור אגבי', 'לא מוזכר'];
H.REL = ['גבוהה', 'בינונית', 'נמוכה'];
H.EVENTS = [ // אירועי רקע כלליים (ידע היסטורי כללי, לא נגזר מהגיליון)
  ['1905-01-22', 'יום ראשון הדמים (רוסיה)'], ['1905-03-31', 'ביקור הקייזר בטנג׳יר'],
  ['1906-01-16', 'ועידת אלג׳סיראס'], ['1907-08-05', 'הפצצת קזבלנקה'],
  ['1908-07-24', 'מהפכת התורכים הצעירים'], ['1911-07-01', 'משבר אגאדיר'],
  ['1911-09-29', 'המלחמה האיטלקית־טורקית'], ['1912-03-30', 'הסכם פאס'],
  ['1912-10-08', 'מלחמת הבלקן הראשונה'], ['1913-10-01', 'משפט בייליס'],
  ['1914-07-28', 'פרוץ מלחמת העולם הראשונה'], ['1917-03-15', 'מהפכת פברואר']
];
H.pcol = p => (H.PAPERS[p] || {}).color || '#888';
H.pname = p => (H.PAPERS[p] || {}).he || p;

/* ====== נרמול טקסט (עברית + יידיש) ====== */
const FIN = { 'ך': 'כ', 'ם': 'מ', 'ן': 'נ', 'ף': 'פ', 'ץ': 'צ' };
const YM = { '\u05f0': 'וו', '\u05f1': 'וי', '\u05f2': 'יי' };
const DROP = /[\u05f3\u05f4"'`’‘“”׳״⟦⟧\u200e\u200f]/;
const MARKS = /[\u0300-\u036f\u05b0-\u05c7]/;
function nc(ch) {
  const c = ch.charCodeAt(0);
  if (c >= 0x5d0 && c <= 0x5ea) return FIN[ch] || ch;
  if (c >= 97 && c <= 122 || c >= 48 && c <= 57) return ch;
  if (c === 32 || c === 10 || c === 13 || c === 9) return ' ';
  if (c >= 65 && c <= 90) return ch.toLowerCase();
  let o = '';
  for (const x of ch.normalize('NFKD')) {
    if (MARKS.test(x) || DROP.test(x)) continue;
    if (YM[x] !== undefined) { o += YM[x]; continue; }
    if (FIN[x]) { o += FIN[x]; continue; }
    if (/[\p{L}\p{N}]/u.test(x)) o += x.toLowerCase(); else o += ' ';
  }
  return o;
}
function normMap(s) {
  let n = '', map = [];
  for (let i = 0; i < s.length; i++) { const x = nc(s[i]); for (let j = 0; j < x.length; j++) { n += x[j]; map.push(i); } }
  return { n, map };
}
const norm = s => normMap(String(s ?? '')).n.replace(/\s+/g, ' ').trim();
const toks = q => norm(q).split(' ').filter(Boolean);

/* הדגשת חיפוש בטקסט מקורי */
function highlight(text, tokens) {
  text = String(text ?? '');
  if (!tokens || !tokens.length) return esc(text);
  const { n, map } = normMap(text);
  const ranges = [];
  for (const t of tokens) {
    let i = 0;
    while ((i = n.indexOf(t, i)) !== -1) { ranges.push([map[i], map[i + t.length - 1] + 1]); i += t.length; }
  }
  if (!ranges.length) return esc(text);
  ranges.sort((a, b) => a[0] - b[0]);
  const merged = [];
  for (const r of ranges) { const l = merged[merged.length - 1]; if (l && r[0] <= l[1]) l[1] = Math.max(l[1], r[1]); else merged.push([...r]); }
  let out = '', p = 0;
  for (const [a, b] of merged) { out += esc(text.slice(p, a)) + '<mark>' + esc(text.slice(a, b)) + '</mark>'; p = b; }
  return out + esc(text.slice(p));
}

/* ====== תאריכים ====== */
const MONTHS = ['ינואר', 'פברואר', 'מרץ', 'אפריל', 'מאי', 'יוני', 'יולי', 'אוגוסט', 'ספטמבר', 'אוקטובר', 'נובמבר', 'דצמבר'];
function fmtDate(iso) { if (!iso) return ''; const [y, m, d] = iso.split('-').map(Number); return `${d} ב${MONTHS[m - 1]} ${y}`; }
function fmtMonth(k) { const [y, m] = k.split('-').map(Number); return `${MONTHS[m - 1]} ${y}`; }
const dayNum = iso => { const [y, m, d] = iso.split('-').map(Number); return Date.UTC(y, m - 1, d) / 864e5; };

/* דליי זמן */
function bucketKey(iso, gran) {
  const y = iso.slice(0, 4), m = +iso.slice(5, 7);
  if (gran === 'year') return y;
  if (gran === 'quarter') return y + '-Q' + Math.ceil(m / 3);
  return iso.slice(0, 7);
}
function bucketLabel(k) {
  if (/^\d{4}$/.test(k)) return k;
  if (/Q/.test(k)) { const [y, q] = k.split('-Q'); return `רבעון ${q} ${y}`; }
  return fmtMonth(k);
}
function allBuckets(gran) {
  const y0 = +H.minD.slice(0, 4), y1 = +H.maxD.slice(0, 4), out = [];
  for (let y = y0; y <= y1; y++) {
    if (gran === 'year') out.push(String(y));
    else if (gran === 'quarter') for (let q = 1; q <= 4; q++) out.push(`${y}-Q${q}`);
    else for (let m = 1; m <= 12; m++) out.push(`${y}-${String(m).padStart(2, '0')}`);
  }
  // חיתוך שוליים ריקים
  const used = new Set(H.A.map(a => bucketKey(a.d, gran)));
  let s = 0, e = out.length - 1;
  while (s < e && !used.has(out[s])) s++;
  while (e > s && !used.has(out[e])) e--;
  return out.slice(s, e + 1);
}
const monthEnd = ym => { const [y, m] = ym.split('-').map(Number); return ym + '-' + String(new Date(y, m, 0).getDate()).padStart(2, '0'); };
function bucketRange(k) { // [from,to] כמחרוזות ISO
  if (/^\d{4}$/.test(k)) return [k + '-01-01', k + '-12-31'];
  if (/Q/.test(k)) { const [y, q] = k.split('-Q'); const m0 = (q - 1) * 3 + 1; return [`${y}-${String(m0).padStart(2, '0')}-01`, monthEnd(`${y}-${String(m0 + 2).padStart(2, '0')}`)]; }
  return [k + '-01', monthEnd(k)];
}

/* ====== טעינה ואינדקס ====== */
H.load = async function () {
  const r = await fetch('data.json', { cache: 'no-cache' });
  if (!r.ok) throw new Error('data.json: ' + r.status);
  return H.init(await r.json());
};
H.init = function (D) {
  H.meta = D.meta; H.ents = D.ents; H.A = D.arts; H.rels = D.rels || [];
  for (const t of Object.keys(H.TYPES)) H.ents[t] = H.ents[t] || {};
  H.typeOf = id => { const t = String(id).replace(/^\?/, '').split(':')[0]; return H.TYPES[t] ? t : null; };
  H.info = id => { const t = H.typeOf(id); return t ? H.ents[t][id] : null; };
  H.label = id => { const e = H.info(id); return e ? e.h : id; };
  // היררכיה: אבות (נושא-אב, מקום מכיל, קבוצה רחבה) ותתי-ישויות
  const ancMemo = new Map();
  H.anc = id => {
    if (ancMemo.has(id)) return ancMemo.get(id);
    const out = [], st = [...((H.info(id) || {}).up || [])];
    while (st.length) { const x = st.pop(); if (x === id || out.includes(x)) continue; out.push(x); st.push(...((H.info(x) || {}).up || [])); }
    ancMemo.set(id, out); return out;
  };
  H.kids = new Map();
  for (const t of Object.keys(H.TYPES)) for (const [id, e] of Object.entries(H.ents[t])) for (const u of e.up || []) { if (!H.kids.has(u)) H.kids.set(u, []); H.kids.get(u).push(id); }
  H.relOut = new Map(); H.relIn = new Map();
  for (const [s, p, o, w] of H.rels) {
    if (!H.relOut.has(s)) H.relOut.set(s, []); H.relOut.get(s).push([p, o, w]);
    if (!H.relIn.has(o)) H.relIn.set(o, []); H.relIn.get(o).push([p, s, w]);
  }
  H.themeName = Object.fromEntries(D.meta.themes.map(t => [t.k, t.h]));
  H.themeKeys = D.meta.themes.map(t => t.k);
  H.minD = H.A[0].d; H.maxD = H.A[H.A.length - 1].d;
  const nk = H.nk = h => { // זהה ל-norm_key בפייתון
    h = h.replace(/[\u05f3\u05f4"'`’‘“”]/g, '').replace(/[־-]/g, ' ').replace(/\s+/g, ' ').trim();
    if (h.length > 3 && h[0] === 'ה') h = h.slice(1);
    return h;
  };
  const entText = id => { const e = H.info(id) || { h: id, y: [] }; return [e.h, ...(e.y || []), ...(e.a || []), e.en || ''].join(' '); };
  for (const a of H.A) {
    H.byId.set(a.id, a);
    for (const t of Object.keys(H.TYPES)) {
      a['k_' + t] = a[t] || [];                                   // מזהי ישויות
      a[t] = a['k_' + t].map(id => { const e = H.ents[t][id] || { h: id, y: [] }; return [e.h, (e.y || [])[0] || '']; }); // לתצוגה
    }
    a.tr = a.tr || []; a.cn = a.cn || [];
    const own = Object.keys(H.TYPES).flatMap(t => a['k_' + t]);
    a._anc = new Set(own); for (const id of own) for (const x of H.anc(id)) a._anc.add(x);
    for (const x of a.cn) a._anc.add(x);
    a._sum = norm(a.s + ' ' + a.c);
    for (const t of Object.keys(H.TYPES)) a['_' + t] = norm(a['k_' + t].map(entText).join(' ; ') + (t === 'top' ? ' ; ' + a.tr.join(' ; ') : ''));
    a._top = a._top + ' ' + a._ev;
    a._all = [a._sum, a._top, a._ppl, a._pl, a._org, a._grp].join(' | ');
    a._ts = dayNum(a.d);
  }
  // אינדקס ישויות: arts = כולל תתי-ישויות (מרוקו כוללת את פאס; נושא כולל את תתי-הנושאים והאירועים שלו)
  for (const t of Object.keys(H.TYPES)) {
    const m = new Map();
    const get = (k, a) => {
      let e = m.get(k);
      if (!e) { const info = H.ents[t][k] || { h: k, y: [] }; e = { key: k, type: t, h: info.h, y: info.y || [], info, arts: [], direct: 0, papers: {}, first: a.d, last: a.d, byYear: {}, _n: norm(entText(k)) }; m.set(k, e); }
      return e;
    };
    for (const a of H.A) {
      for (const k of a['k_' + t]) get(k, a).direct++;
      for (const k of a._anc) {
        if (H.typeOf(k) !== t) continue;
        const e = get(k, a);
        e.arts.push(a); e.papers[a.p] = (e.papers[a.p] || 0) + 1; e.last = a.d;
        const y = a.d.slice(0, 4); e.byYear[y] = (e.byYear[y] || 0) + 1;
      }
    }
    H.idx[t] = m;
    for (const e of m.values()) { e.count = e.arts.length; if (e.arts.length) e.first = e.arts[0].d; }
  }
  H.countries = [...new Set(H.A.flatMap(a => a.cn))].map(k => ({ k, h: H.label(k), n: H.A.filter(a => a.cn.includes(k)).length })).sort((a, b) => b.n - a.n);
  H.years = []; for (let y = +H.minD.slice(0, 4); y <= +H.maxD.slice(0, 4); y++) H.years.push(String(y));
  H.paperKeys = Object.keys(H.PAPERS).filter(p => H.A.some(a => a.p === p));
  H.paperRange = {}; for (const p of H.paperKeys) { const l = H.A.filter(a => a.p === p); H.paperRange[p] = [l[0].d, l[l.length - 1].d]; }
  return H;
};
H.entity = (t, k) => H.idx[t].get(k);

/* OCR נטען לפי דרישה */
H.loadOCR = async function (onprog) {
  if (H.ocr) return H.ocr;
  if (!H._ocrP) H._ocrP = fetch('ocr.json').then(r => { if (!r.ok) throw new Error('ocr.json'); return r.json(); }).then(j => { H.ocr = j; return j; });
  return H._ocrP;
};
H.ensureOcrNorm = async function (onprog) {
  await H.loadOCR();
  if (H.ocrN) return;
  H.ocrN = {};
  let i = 0;
  while (i < H.A.length) {
    const end = Math.min(i + 20, H.A.length);
    for (; i < end; i++) H.ocrN[H.A[i].id] = norm(H.ocr[H.A[i].id] || '');
    if (onprog) onprog(i / H.A.length);
    await new Promise(r => setTimeout(r, 0));
  }
};

/* ====== סינון ====== */
H.newF = () => ({ q: '', scope: 'all', mode: 'all', papers: new Set(H.paperKeys), from: '', to: '', genre: new Set(), cen: new Set(), rel: new Set(), pt: '', th: '', cn: '', ents: [], jw: 0, deep: 1 });
/* האם הכתבה מתויגת בישות (ובמצב "deep" גם באחת מתתי-הישויות שלה) */
H.has = (a, e, deep = true) => deep ? a._anc.has(e.key) : a['k_' + e.type].includes(e.key);
H.qMatch = function (a, F) {
  const t = toks(F.q);
  if (!t.length) return true;
  let hay;
  switch (F.scope) {
    case 'sum': hay = a._sum; break;
    case 'ocr': hay = (H.ocrN && H.ocrN[a.id]) || ''; break;
    case 'all': hay = a._all; break;
    default: hay = a['_' + F.scope] || '';
  }
  if (F.mode === 'phrase') return hay.includes(t.join(' '));
  if (F.mode === 'any') return t.some(x => hay.includes(x));
  return t.every(x => hay.includes(x));
};
H.filter = function (F, skip) {
  return H.A.filter(a => {
    if (skip !== 'paper' && !F.papers.has(a.p)) return false;
    if (F.from && a.d < F.from) return false;
    if (F.to && a.d > F.to) return false;
    if (skip !== 'genre' && F.genre.size && !F.genre.has(a.g)) return false;
    if (skip !== 'cen' && F.cen.size && !F.cen.has(a.m)) return false;
    if (skip !== 'rel' && F.rel.size && !F.rel.has(a.r)) return false;
    if (F.pt && a.pt !== F.pt) return false;
    if (skip !== 'th' && F.th && !a.th.includes(F.th)) return false;
    if (skip !== 'cn' && F.cn && !a.cn.includes(F.cn)) return false;
    if (F.jw && !a.jw) return false;
    for (const e of F.ents) if (!H.has(a, e, F.deep !== 0)) return false;
    return H.qMatch(a, F);
  });
};
H.sorters = {
  dateAsc: (a, b) => a.d.localeCompare(b.d) || a.n - b.n,
  dateDesc: (a, b) => b.d.localeCompare(a.d) || a.n - b.n,
  relDesc: (a, b) => H.REL.indexOf(a.r) - H.REL.indexOf(b.r) || H.CEN.indexOf(a.m) - H.CEN.indexOf(b.m) || a.d.localeCompare(b.d)
};

/* ====== ייצוא CSV ====== */
H.toCSV = function (head, rows) {
  const q = v => { v = v == null ? '' : String(v); return /[",\n\r]/.test(v) ? '"' + v.replace(/"/g, '""') + '"' : v; };
  return '\ufeff' + [head, ...rows].map(r => r.map(q).join(',')).join('\r\n');
};
H.download = function (name, text, type = 'text/csv;charset=utf-8') {
  const url = URL.createObjectURL(new Blob([text], { type }));
  const a = document.createElement('a'); a.href = url; a.download = name; document.body.appendChild(a); a.click(); a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 2000);
};
H.artsCSV = function (list, name = 'articles') {
  const names = x => x.map(([h]) => h).join(' ; ');
  const head = ['מזהה', 'עיתון', 'תאריך', 'קישור לספרייה הלאומית', 'סוגה', 'מרכזיות המונח', 'רלוונטיות', 'נושא-על ראשי', 'סיכום', 'מה נאמר על המונח', 'נושאים', 'אירועים', 'אנשים', 'מקומות', 'ארגונים', 'קבוצות אוכלוסייה', 'מדינות', 'נושאים (ניסוח מקורי)', 'מזהי ישויות'];
  const rows = list.map(a => [a.id, H.pname(a.p), a.d, a.u, a.g, a.m, a.r, H.themeName[a.pt], a.s, a.c, names(a.top), names(a.ev), names(a.ppl), names(a.pl), names(a.org), names(a.grp), a.cn.map(H.label).join(' ; '), a.tr.join(' ; '), Object.keys(H.TYPES).flatMap(t => a['k_' + t]).join(' ; ')]);
  H.download(name + '.csv', H.toCSV(head, rows));
};

/* ====== טיפ ====== */
H.tip = function (node, fn) {
  const t = $('#tip');
  node.addEventListener('mouseenter', e => { t.innerHTML = fn(); t.style.display = 'block'; });
  node.addEventListener('mousemove', e => { t.style.left = Math.min(e.clientX + 14, innerWidth - 290) + 'px'; t.style.top = (e.clientY + 16) + 'px'; });
  node.addEventListener('mouseleave', () => { t.style.display = 'none'; });
};

/* ====== בניית DOM קצרה ====== */
function h(tag, attrs, ...kids) {
  const e = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs || {})) {
    if (v == null || v === false) continue;
    if (k === 'class') e.className = v; else if (k === 'html') e.innerHTML = v;
    else if (k.startsWith('on')) e.addEventListener(k.slice(2), v);
    else if (k === 'style' && typeof v === 'object') { for (const [sk, sv] of Object.entries(v)) sk.startsWith('--') ? e.style.setProperty(sk, sv) : (e.style[sk] = sv); }
    else e.setAttribute(k, v === true ? '' : v);
  }
  for (const k of kids.flat()) if (k != null && k !== false) e.append(k.nodeType ? k : document.createTextNode(k));
  return e;
}
const NS = 'http://www.w3.org/2000/svg';
function S(tag, attrs, ...kids) {
  const e = document.createElementNS(NS, tag);
  for (const [k, v] of Object.entries(attrs || {})) { if (v == null) continue; if (k.startsWith('on')) e.addEventListener(k.slice(2), v); else e.setAttribute(k, v); }
  for (const k of kids.flat()) if (k != null) e.append(k.nodeType ? k : document.createTextNode(k));
  return e;
}
