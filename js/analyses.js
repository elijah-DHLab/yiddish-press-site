'use strict';
/* ====== תמונה היסטורית רחבה: 15 שאלות על הדאטה ====== */
const TH_PAL = ['#c0562c', '#7b4ea3', '#2a7f62', '#a83a4f', '#5b6770', '#2f6db5', '#d29a1f', '#16899e', '#6aa84f', '#8e6c4a', '#b3a037', '#c2679a', '#3d4f8f', '#e07b39', '#4f8a8b', '#9c6644', '#7d8f3a', '#b5838d', '#355070', '#6d597a'];
const thCol = k => k === 'other' ? '#aaaaaa' : TH_PAL[Math.max(0, H.themeKeys.indexOf(k)) % TH_PAL.length];
const CEN_COL = ['#183445', '#3b7ea1', '#9fc3d6', '#c9c9c9'];
const GEN_COL = ['#25485c', '#c0562c', '#6aa84f', '#7b4ea3', '#d29a1f', '#aaaaaa'];
const SEARCH_PLACES = ['pl:morocco', 'pl:fez', 'pl:marrakesh', 'pl:damascus', 'pl:thessaloniki'];
const pSeries = () => H.paperKeys.map(p => ({ key: p, label: H.pname(p), color: H.pcol(p) }));
const ofP = p => H.A.filter(a => a.p === p);
const yearOf = a => a.d.slice(0, 4);
const entArts = (t, k) => (H.entity(t, k) || { arts: [] }).arts;
const rangeFilter = k => { const [f, t] = bucketRange(k); return { from: f, to: t }; };

const AN = [];
const reg = (title, how, draw, o = {}) => AN.push({ title, how, draw, wide: !!o.wide });

/* 1 */
reg('כמה נכתב, ומתי?', 'מספר הכתבות בדגימה לפי חודש ולפי עיתון. הקווים הכתומים הם אירועי רקע. לחיצה על עמודה פותחת את הכתבות.', host => {
  const buckets = allBuckets('month'), idx = new Map(buckets.map((k, i) => [k, i])), series = pSeries();
  const cell = buckets.map(() => ({}));
  for (const a of H.A) { const i = idx.get(a.d.slice(0, 7)); (cell[i][a.p] = cell[i][a.p] || []).push(a); }
  H.timeBars(host, { buckets, series, gran: 'month', events: true, height: 200, cell: (bi, si) => cell[bi][series[si].key] || [], aria: 'כתבות לפי חודש',
    onClick: (arts, k, s) => H.openList({ title: `${s.label} · ${bucketLabel(k)}`, arts, filter: { papers: [s.key], ...rangeFilter(k) } }) });
  const tot = buckets.map((k, i) => [k, Object.values(cell[i]).reduce((s, l) => s + l.length, 0)]).sort((a, b) => b[1] - a[1]);
  const y = {}; for (const a of H.A) y[yearOf(a)] = (y[yearOf(a)] || 0) + 1; const ty = Object.entries(y).sort((a, b) => b[1] - a[1])[0];
  return { read: `החודש העמוס ביותר: ${bucketLabel(tot[0][0])} (${nf(tot[0][1])} כתבות). השנה העמוסה ביותר: ${ty[0]} עם ${nf(ty[1])} כתבות, ${pct(ty[1], H.A.length)}% מהדגימה. הנפח מושפע ממונחי האיסוף.`,
    table: { head: ['חודש', ...series.map(s => s.label)], rows: buckets.map((k, i) => [k, ...series.map(s => (cell[i][s.key] || []).length)]) } };
}, { wide: true });

/* 2 */
reg('מרוקו, דמשק, סלוניקי: מתי כל מקום עלה?', 'כמה כתבות בכל רבעון מזכירות כל אחד משלושת המקומות (לפי שדה "מקומות"), בכל העיתונים יחד. לחיצה על נקודה פותחת את הכתבות.', host => {
  const keys = ['pl:morocco', 'pl:damascus', 'pl:thessaloniki'].filter(k => H.entity('pl', k)), col = { 'pl:morocco': '#d35400', 'pl:damascus': '#6c3483', 'pl:thessaloniki': '#117a65' };
  const buckets = allBuckets('quarter'), idx = new Map(buckets.map((k, i) => [k, i]));
  const cell = keys.map(() => buckets.map(() => []));
  keys.forEach((k, ki) => { for (const a of entArts('pl', k)) { const i = idx.get(bucketKey(a.d, 'quarter')); if (i != null) cell[ki][i].push(a); } });
  const series = keys.map((k, ki) => ({ key: k, label: H.label(k), color: col[k], vals: cell[ki].map(l => l.length) }));
  const lg = h('div', { class: 'legend' }, series.map(s => h('span', {}, h('i', { class: 'dot', style: { background: s.color } }), s.label)));
  const ch = h('div'); host.append(lg, ch);
  H.lineChart(ch, { buckets, gran: 'quarter', height: 210, series, events: true, aria: 'מקומות לאורך זמן', onClick: (s, i) => H.openList({ title: `${s.label} · ${bucketLabel(buckets[i])}`, arts: cell[keys.indexOf(s.key)][i], filter: { ents: [{ type: 'pl', key: s.key }], ...rangeFilter(buckets[i]) } }) });
  const pk = series.map(s => { const m = Math.max(...s.vals); return `${s.label}: שיא ב${bucketLabel(buckets[s.vals.indexOf(m)])} (${m})`; });
  return { read: pk.join(' · '), table: { head: ['רבעון', ...keys.map(H.label)], rows: buckets.map((k, i) => [k, ...keys.map((_, ki) => cell[ki][i].length)]) } };
});

/* 3 */
reg('האם המקום במרכז הכתבה, או רק אגב?', 'שדה "מרכזיות המונח": האם מונח החיפוש הוא נושא הכתבה, ידיעה אחת מתוך כמה, או אזכור אגבי. 100% לכל עיתון ולכל שנה.', host => {
  const cats = H.CEN.map((c, i) => ({ label: c, color: CEN_COL[i], test: a => a.m === c }));
  const rows = [...H.paperKeys.map(p => ({ label: H.pname(p), arts: ofP(p), filter: { papers: [p] } })), ...H.years.map(y => ({ label: y, arts: H.A.filter(a => yearOf(a) === y), filter: { from: y + '-01-01', to: y + '-12-31' } }))].filter(r => r.arts.length);
  H.stack100(host, rows, cats, { onSeg: (r, c, arts) => H.openList({ title: `${r.label} · ${c.label}`, arts, filter: { ...r.filter, cen: [c.label] } }) });
  const c = k => H.A.filter(a => a.m === k).length;
  return { read: `${pct(c(H.CEN[0]) + c(H.CEN[1]), H.A.length)}% מהכתבות עוסקות במונח כנושא או כידיעה עצמאית; ${pct(c(H.CEN[2]), H.A.length)}% אזכורים אגביים; ${nf(c(H.CEN[3]))} כתבות שבהן המונח לא נמצא בפועל (התאמות OCR שגויות).`,
    table: { head: ['שורה', 'סה״כ', ...H.CEN], rows: rows.map(r => [r.label, r.arts.length, ...H.CEN.map(k => r.arts.filter(a => a.m === k).length)]) } };
});

/* 4 */
reg('אילו סוגות עיתונאיות?', 'חדשות, דעה, התכתבות, ספרותי ועוד, כאחוז מכתבות כל עיתון.', host => {
  const gc = {}; for (const a of H.A) gc[a.g] = (gc[a.g] || 0) + 1;
  const gs = Object.keys(gc).filter(Boolean).sort((a, b) => gc[b] - gc[a]);
  const cats = gs.map((g, i) => ({ label: g, color: GEN_COL[i % GEN_COL.length], test: a => a.g === g }));
  const rows = H.paperKeys.map(p => ({ label: H.pname(p), arts: ofP(p) }));
  H.stack100(host, rows, cats, { onSeg: (r, c, arts) => H.openList({ title: `${r.label} · ${c.label}`, arts, filter: { papers: [H.paperKeys[rows.indexOf(r)]], genre: [c.label] } }) });
  const top = H.paperKeys.map(p => { const l = ofP(p), o = gs.map(g => [g, l.filter(a => a.g === g).length]).sort((a, b) => b[1] - a[1]); return `${H.pname(p)}: ${o[0][0]} ${pct(o[0][1], l.length)}%`; });
  return { read: top.join(' · '), table: { head: ['עיתון', ...gs], rows: rows.map(r => [r.label, ...gs.map(g => r.arts.filter(a => a.g === g).length)]) } };
});

/* 5 */
reg('על מה מדברים? נושאי-על לפי עיתון', 'הנושא הראשי של כל כתבה (ענף השורש של אוצר המילים שאליו שייכים רוב נושאיה) כאחוז מכתבות העיתון. הצבע כהה = חלק גדול יותר. לחיצה על תא פותחת את הכתבות.', host => {
  const themes = H.themeKeys.filter(k => H.A.some(a => a.pt === k)).sort((a, b) => H.A.filter(x => x.pt === b).length - H.A.filter(x => x.pt === a).length);
  const rowL = themes.map(k => ({ label: H.themeName[k], k })), colL = H.paperKeys.map(p => ({ label: H.pname(p), p }));
  H.heat(host, rowL, colL, (r, c) => { const arts = H.A.filter(a => a.p === colL[c].p && a.pt === rowL[r].k); return { v: arts.length / (ofP(colL[c].p).length || 1), arts }; },
    { onClick: (r, c, arts) => H.openList({ title: `${c.label} · ${r.label}`, arts, filter: { papers: [c.p], pt: r.k } }) });
  const tops = colL.map(c => { const o = themes.map(k => [k, H.A.filter(a => a.p === c.p && a.pt === k).length]).sort((a, b) => b[1] - a[1])[0]; return `${c.label}: ${H.themeName[o[0]]} (${pct(o[1], ofP(c.p).length)}%)`; });
  return { read: 'הנושא הראשי הגדול בכל עיתון: ' + tops.join(' · '), table: { head: ['נושא-על', ...colL.map(c => c.label)], rows: rowL.map(r => [r.label, ...colL.map(c => H.A.filter(a => a.p === c.p && a.pt === r.k).length)]) } };
});

/* 6 */
let themeMode = 'pct';
reg('איך השתנו הנושאים לאורך השנים?', 'הרכב נושאי-העל הראשיים בכל שנה, באחוזים או במספרים.', (host, again) => {
  const themes = H.themeKeys.filter(k => H.A.some(a => a.pt === k));
  const series = themes.map(k => ({ key: k, label: H.themeName[k], color: thCol(k) }));
  const buckets = H.years.filter(y => H.A.some(a => yearOf(a) === y));
  const bar = h('div', { class: 'seg', style: { maxWidth: '240px', marginBottom: '8px' } }, [['pct', 'באחוזים'], ['abs', 'במספרים']].map(([k, l]) => h('button', { class: themeMode === k ? 'on' : '', onclick: () => { themeMode = k; again(); } }, l)));
  const ch = h('div'); host.append(bar, ch);
  H.timeBars(ch, { buckets, series, gran: 'year', yMode: themeMode, height: 230, aria: 'נושאים לפי שנה', cell: (bi, si) => H.A.filter(a => yearOf(a) === buckets[bi] && a.pt === themes[si]),
    onClick: (arts, y, s) => H.openList({ title: `${y} · ${s.label}`, arts, filter: { from: y + '-01-01', to: y + '-12-31', pt: s.key } }) });
  host.append(h('div', { class: 'legend' }, series.map(s => h('span', {}, h('i', { class: 'dot', style: { background: s.color } }), s.label))));
  const wwk = H.themeKeys.find(k => /world-war/.test(k)), ww = H.A.filter(a => a.pt === wwk), first = ww.length ? ww[0].d : null;
  return { read: first ? `הכתבות הראשונות שנושאן הראשי הוא מלחמת העולם הראשונה: ${fmtDate(first)}. ${nf(ww.length)} כתבות בסך הכול.` : '', table: { head: ['שנה', ...series.map(s => s.label)], rows: buckets.map(y => [y, ...themes.map(k => H.A.filter(a => yearOf(a) === y && a.pt === k).length)]) } };
}, { wide: true });

/* 7 */
const STOP = new Set('של על את בין עם מול לפי אל כל אחר אחרים אחרת ועוד בעקבות בנוגע לגבי תחת מתוך אחד אחת שני שתי חדשות שונות שונים כללי כללית כלליות ידיעות ידיעה אחרות או גם לא זה זו הוא היא מן אך כי אם עד אצל ללא בשל ליד נגד העולם הראשונה שאלת יחסי מדיניות'.split(' ').map(norm));
reg('אילו מילים חוזרות בנושאי הכתבות?', 'תדירות מילים בניסוח החופשי של שדה "נושאים" בגיליון (כמה כתבות מכילות את המילה), בפילוח לפי עיתון. לחיצה על מילה מחפשת אותה בנושאים; לחיצה על קטע פותחת את הכתבות.', host => {
  const raw = new Map(); // מילה → {arts:Set, surf:Counter}
  const tokOf = s => s.split(/[\s,;:.\-־"״()?!]+/).map(w => w.replace(/^['׳]+|['׳]+$/g, '')).filter(Boolean);
  const vocab = new Map();
  for (const a of H.A) for (const t of a.tr) for (const w of tokOf(t)) { const k = norm(w); if (k.length < 3 || STOP.has(k)) continue; let e = vocab.get(k); if (!e) vocab.set(k, e = { arts: new Set(), surf: {} }); e.arts.add(a); e.surf[w] = (e.surf[w] || 0) + 1; }
  // איחוד תחיליות פשוטות (ה/ב/ל/ו) כשהצורה החשופה שכיחה
  for (const [k, e] of [...vocab]) { if (k.length > 4 && 'הבלו'.includes(k[0])) { const b = vocab.get(k.slice(1)); if (b && b.arts.size >= 3) { for (const a of e.arts) b.arts.add(a); vocab.delete(k); } } }
  const rows = [...vocab.entries()].map(([k, e]) => ({ k, label: Object.entries(e.surf).sort((a, b) => b[1] - a[1])[0][0], arts: [...e.arts] })).sort((a, b) => b.arts.length - a.arts.length).slice(0, 34)
    .map(r => ({ ...r, total: r.arts.length, segs: H.paperKeys.map(p => ({ key: p, label: H.pname(p), color: H.pcol(p), value: r.arts.filter(a => a.p === p).length })) }));
  H.hbars(host, rows, { onLabel: r => H.applyFilter({ q: r.k, scope: 'top' }), onSeg: (r, s) => H.openList({ title: `"${r.label}" · ${s.label}`, arts: r.arts.filter(a => a.p === s.key), filter: { q: r.k, scope: 'top', papers: [s.key] } }) });
  host.append(h('div', { class: 'legend' }, pSeries().map(s => h('span', {}, h('i', { class: 'dot', style: { background: s.color } }), s.label))));
  return { read: `המילים השכיחות ביותר: ${rows.slice(0, 6).map(r => r.label).join(', ')}.`, table: { head: ['מילה', 'כתבות', ...H.paperKeys.map(H.pname)], rows: rows.map(r => [r.label, r.total, ...r.segs.map(s => s.value)]) } };
});

/* 8 */
let placesAll = false;
reg('אילו מקומות נכנסים לעולם של כל עיתון?', 'המקומות המוזכרים ביותר בכל עיתון (אזכור ישיר), כאחוז מכתבותיו. כברירת מחדל ללא מקומות האיסוף עצמם (מרוקו, פאס, מראכש, דמשק, סלוניקי).', (host, again) => {
  const cb = h('label', { class: 'fopt', style: { marginBottom: '8px' } }, h('input', { type: 'checkbox', checked: placesAll, onchange: e => { placesAll = e.target.checked; again(); } }), 'כולל מקומות האיסוף');
  const grid = h('div', { style: { display: 'grid', gridTemplateColumns: 'repeat(auto-fit,minmax(260px,1fr))', gap: '16px' } });
  host.append(cb, grid);
  const table = [];
  for (const p of H.paperKeys) {
    const arts = ofP(p), cnt = new Map();
    for (const a of arts) for (const k of a.k_pl) { if (!placesAll && SEARCH_PLACES.includes(k)) continue; cnt.set(k, (cnt.get(k) || 0) + 1); }
    const top = [...cnt.entries()].sort((a, b) => b[1] - a[1]).slice(0, 12);
    const rows = top.map(([k, n]) => ({ label: H.entity('pl', k).h, k, total: n, denom: arts.length, segs: [{ key: p, label: H.pname(p), color: H.pcol(p), value: n }] }));
    const col = h('div', {}, h('div', { style: { display: 'flex', gap: '8px', borderBottom: '3px solid ' + H.pcol(p), paddingBottom: '4px', marginBottom: '6px', fontWeight: 700 } }, H.pname(p), h('span', { class: 'muted small' }, nf(arts.length) + ' כתבות')));
    const hb = h('div'); col.append(hb); grid.append(col);
    H.hbars(hb, rows, { fmt: r => pct(r.total, r.denom) + '%', onLabel: r => H.openList({ title: `${H.pname(p)} · ${r.label}`, arts: arts.filter(a => a.k_pl.includes(r.k)), filter: { papers: [p], ents: [{ type: 'pl', key: r.k }] } }), onSeg: r => H.openList({ title: `${H.pname(p)} · ${r.label}`, arts: arts.filter(a => a.k_pl.includes(r.k)), filter: { papers: [p], ents: [{ type: 'pl', key: r.k }] } }) });
    top.forEach(([k, n]) => table.push([H.pname(p), H.entity('pl', k).h, n, pct(n, arts.length)]));
  }
  return { read: 'מי שמופיע בכמה עיתונים בראש הרשימה מצביע על אזורי עניין משותפים; מקום שבולט רק בעיתון אחד מעיד על דגש מקומי או על דגימת האיסוף.', table: { head: ['עיתון', 'מקום', 'כתבות', '% מכתבות העיתון'], rows: table } };
}, { wide: true });

/* 9 */
reg('אישים: מי מופיע, ומתי?', '14 האישים המוזכרים ביותר. כל נקודה היא חודש-עיתון שבו הוזכר האיש (גודל = מספר כתבות). לחיצה על נקודה פותחת את הכתבות, ולחיצה על השם פותחת את כל כתבותיו.', host => {
  const top = [...H.idx.ppl.values()].sort((a, b) => b.count - a.count).slice(0, 14);
  const rows = top.map(e => ({ label: e.h, arts: e.arts, key: e.key }));
  H.dotTimeline(host, rows, { onDot: (arts, r) => H.openList({ title: `${r.label} · ${fmtMonth(arts[0].d.slice(0, 7))} · ${H.pname(arts[0].p)}`, arts }), onRow: r => H.openList({ title: r.label, arts: r.arts, filter: { ents: [{ type: 'ppl', key: r.key }] } }) });
  host.append(h('div', { class: 'legend' }, pSeries().map(s => h('span', {}, h('i', { class: 'dot', style: { background: s.color } }), s.label))));
  return { read: `${top[0].h} (${top[0].count} כתבות), ${top[1].h} (${top[1].count}), ${top[2].h} (${top[2].count}). תארים כמו "הסולטאן" או "הקיסר" שויכו לאדם לפי תאריך הכתבה והקשרה.`, table: { head: ['אדם', 'כתבות', 'ראשונה', 'אחרונה'], rows: top.map(e => [e.h, e.count, e.first, e.last]) } };
});

/* 10, 11 */
function entBars(type, n, read) {
  return host => {
    const top = [...H.idx[type].values()].sort((a, b) => b.count - a.count).slice(0, n);
    const rows = top.map(e => ({ label: e.h, e, total: e.count, segs: H.paperKeys.map(p => ({ key: p, label: H.pname(p), color: H.pcol(p), value: e.papers[p] || 0 })) }));
    const open = (r, p) => H.openList({ title: p ? `${r.label} · ${H.pname(p)}` : r.label, arts: p ? r.e.arts.filter(a => a.p === p) : r.e.arts, filter: { ents: [{ type, key: r.e.key }], ...(p ? { papers: [p] } : {}) } });
    H.hbars(host, rows, { onLabel: r => open(r), onSeg: (r, s) => open(r, s.key) });
    host.append(h('div', { class: 'legend' }, pSeries().map(s => h('span', {}, h('i', { class: 'dot', style: { background: s.color } }), s.label))));
    return { read: read(top), table: { head: [H.TYPE1[type], 'כתבות', ...H.paperKeys.map(H.pname)], rows: top.map(e => [e.h, e.count, ...H.paperKeys.map(p => e.papers[p] || 0)]) } };
  };
}
reg('אילו מוסדות וארגונים עולים?', 'הארגונים והמוסדות המוזכרים ביותר, בפילוח לפי עיתון.', entBars('org', 18, t => `בראש: ${t.slice(0, 4).map(e => e.h).join(', ')}. מוסדות פרלמנטריים ושלטוניים מככבים, וארגונים יהודיים נמצאים מאחוריהם.`));
reg('מי נמצא בכתבות? קבוצות אוכלוסייה', 'קבוצות האוכלוסייה המוזכרות בכתבות, בפילוח לפי עיתון.', entBars('grp', 18, t => { const j = H.entity('grp', 'grp:jews'); return `בראש: ${t.slice(0, 4).map(e => e.h).join(', ')}.` + (j ? ` "יהודים" מופיעים ב־${pct(j.count, H.A.length)}% מהכתבות.` : ''); }));

/* 12 */
let netMin = 8;
reg('רשת מקומות: אילו מקומות נזכרים יחד?', 'כל עיגול הוא מקום (גודל = מספר כתבות), וכל קו מציין כתבות שבהן שני המקומות נזכרים יחד (עובי = כמות). הזיזו את המחוון כדי להציג רק קשרים חזקים. לחיצה על עיגול או קו פותחת את הכתבות.', (host, again) => {
  const top = [...H.idx.pl.values()].sort((a, b) => b.count - a.count).slice(0, 38);
  const set = new Set(top.map(e => e.key)), w = new Map();
  for (const a of H.A) { const ks = a.k_pl.filter(k => set.has(k)); for (let i = 0; i < ks.length; i++) for (let j = i + 1; j < ks.length; j++) { const key = [ks[i], ks[j]].sort().join('|'); w.set(key, (w.get(key) || 0) + 1); } }
  const sl = h('input', { type: 'range', min: 2, max: 40, value: netMin, 'aria-label': 'סף קשר', style: { width: '200px' } });
  const lab = h('span', { class: 'small' }, `קשרים של ${netMin} כתבות משותפות לפחות`);
  const ch = h('div', { style: { direction: 'ltr' } });
  host.append(h('div', { style: { display: 'flex', gap: '12px', alignItems: 'center', marginBottom: '8px' } }, sl, lab), ch);
  const draw = () => {
    const links = [...w.entries()].filter(([, n]) => n >= netMin).map(([k, n]) => ({ a: k.split('|')[0], b: k.split('|')[1], w: n }));
    const used = new Set(links.flatMap(l => [l.a, l.b]));
    const nodes = top.filter(e => used.has(e.key)).map(e => ({ key: e.key, label: e.h, count: e.count, color: SEARCH_PLACES.includes(e.key) ? '#d35400' : '#25485c' }));
    H.network(ch, nodes, links, { height: 500, onNode: d => H.openList({ title: d.label, arts: entArts('pl', d.key), filter: { ents: [{ type: 'pl', key: d.key }] } }), onLink: (A, B) => H.openList({ title: `${A.label} + ${B.label}`, arts: entArts('pl', A.key).filter(a => a.k_pl.includes(B.key)), filter: { ents: [{ type: 'pl', key: A.key }, { type: 'pl', key: B.key }] } }) });
    return links;
  };
  sl.addEventListener('input', () => { netMin = +sl.value; lab.textContent = `קשרים של ${netMin} כתבות משותפות לפחות`; draw(); });
  const links = draw();
  const best = [...w.entries()].sort((a, b) => b[1] - a[1]).slice(0, 5).map(([k, n]) => `${H.entity('pl', k.split('|')[0]).h}–${H.entity('pl', k.split('|')[1]).h} (${n})`);
  return { read: 'הזוגות הנפוצים ביותר: ' + best.join(', ') + '. כתום = מקומות האיסוף.', table: { head: ['מקום א', 'מקום ב', 'כתבות משותפות'], rows: [...w.entries()].sort((a, b) => b[1] - a[1]).slice(0, 80).map(([k, n]) => [H.entity('pl', k.split('|')[0]).h, H.entity('pl', k.split('|')[1]).h, n]) } };
}, { wide: true });

/* 13 */
let peakSel = 'pl:morocco';
reg('פסגות ואירועי רקע', 'כתבות לפי חודש שבהן מוזכר המקום שנבחר, ולצידן אירועים היסטוריים ידועים (כתום; ידע כללי ולא מן הגיליון). האם הפסגות מתיישבות עם האירועים?', (host, again) => {
  const opts = ['pl:morocco', 'pl:damascus', 'pl:thessaloniki', 'pl:ottoman-empire', 'pl:russian-empire', 'pl:germany', 'pl:france', 'pl:jerusalem'].filter(k => H.entity('pl', k));
  const sel = h('select', { 'aria-label': 'מקום', onchange: e => { peakSel = e.target.value; again(); }, style: { padding: '6px 10px', border: '1px solid var(--line)', borderRadius: '8px', marginBottom: '8px' } }, opts.map(o => h('option', { value: o }, H.label(o))));
  sel.value = peakSel; const ch = h('div'); host.append(sel, ch);
  const buckets = allBuckets('month'), idx = new Map(buckets.map((k, i) => [k, i])), series = pSeries(), cell = buckets.map(() => ({}));
  for (const a of entArts('pl', peakSel)) { const i = idx.get(a.d.slice(0, 7)); (cell[i][a.p] = cell[i][a.p] || []).push(a); }
  H.timeBars(ch, { buckets, series, gran: 'month', events: true, height: 190, cell: (bi, si) => cell[bi][series[si].key] || [], aria: 'פסגות',
    onClick: (arts, k, s) => H.openList({ title: `${H.label(peakSel)} · ${s.label} · ${bucketLabel(k)}`, arts, filter: { papers: [s.key], ents: [{ type: 'pl', key: peakSel }], ...rangeFilter(k) } }) });
  const tot = buckets.map((k, i) => [k, Object.values(cell[i]).reduce((s, l) => s + l.length, 0)]).sort((a, b) => b[1] - a[1]).slice(0, 3);
  return { read: `שלושת החודשים העמוסים ביותר ל"${H.label(peakSel)}": ${tot.map(([k, n]) => `${bucketLabel(k)} (${n})`).join(', ')}.`, table: { head: ['חודש', ...series.map(s => s.label)], rows: buckets.map((k, i) => [k, ...series.map(s => (cell[i][s.key] || []).length)]) } };
}, { wide: true });

/* 14 */
reg('איזה חלק מהכתבות נראה דרך עדשה יהודית?', 'אחוז הכתבות בכל שנה שבהן קבוצות האוכלוסייה כוללות יהודים, או שהנושאים עוסקים ביהודים, בציונות, בקהילות או בעלילות דם (היוריסטיקה גסה, ראו "על הנתונים").', host => {
  const buckets = H.years.filter(y => H.A.some(a => yearOf(a) === y));
  const series = H.paperKeys.map(p => ({ key: p, label: H.pname(p), color: H.pcol(p), vals: buckets.map(y => { const l = H.A.filter(a => a.p === p && yearOf(a) === y); return l.length ? l.filter(a => a.jw).length / l.length * 100 : 0; }), ns: buckets.map(y => H.A.filter(a => a.p === p && yearOf(a) === y)) }));
  host.append(h('div', { class: 'legend' }, series.map(s => h('span', {}, h('i', { class: 'dot', style: { background: s.color } }), s.label))));
  const ch = h('div'); host.append(ch);
  H.lineChart(ch, { buckets, gran: 'year', height: 200, series, ymax: 100, aria: 'עדשה יהודית',
    fmt: (v, s, i) => `${Math.round(v)}% (${s.ns[i].filter(a => a.jw).length} מתוך ${s.ns[i].length})`,
    onClick: (s, i) => H.openList({ title: `${s.label} · ${buckets[i]} · הקשר יהודי`, arts: s.ns[i].filter(a => a.jw), filter: { papers: [s.key], from: buckets[i] + '-01-01', to: buckets[i] + '-12-31', jw: 1 } }) });
  const tot = H.paperKeys.map(p => { const l = ofP(p); return `${H.pname(p)}: ${pct(l.filter(a => a.jw).length, l.length)}%`; });
  return { read: 'סך הכול לפי עיתון: ' + tot.join(' · ') + '. הדגימה כולה נאספה סביב מקומות, וחלקה סביב קהילות יהודיות, ולכן הנתון אינו מדד להטיה של העיתון.', table: { head: ['שנה', ...series.map(s => s.label + ' %')], rows: buckets.map((y, i) => [y, ...series.map(s => Math.round(s.vals[i] * 10) / 10)]) } };
});

/* 15 */
let startPaper = '';
reg('איפה כדאי להתחיל לקרוא?', 'מטריצה של מרכזיות המונח מול הרלוונטיות למחקר. הפינה של "נושא הכתבה" ו"רלוונטיות גבוהה" היא נקודת פתיחה טבעית לקריאה מעמיקה. לחיצה על תא פותחת את הכתבות.', (host, again) => {
  const sel = h('select', { 'aria-label': 'עיתון', onchange: e => { startPaper = e.target.value; again(); }, style: { padding: '6px 10px', border: '1px solid var(--line)', borderRadius: '8px', marginBottom: '8px' } }, h('option', { value: '' }, 'כל העיתונים'), H.paperKeys.map(p => h('option', { value: p }, H.pname(p))));
  sel.value = startPaper; const ch = h('div'); host.append(sel, ch);
  const base = H.A.filter(a => !startPaper || a.p === startPaper);
  const rowL = H.CEN.slice(0, 3).map(c => ({ label: c })), colL = H.REL.map(r => ({ label: 'רלוונטיות ' + r, r }));
  H.heat(ch, rowL, colL, (r, c) => { const arts = base.filter(a => a.m === rowL[r].label && a.r === colL[c].r); return { v: arts.length / (base.length || 1), arts }; },
    { pctFmt: x => nf(x.arts.length), onClick: (r, c, arts) => H.openList({ title: `${r.label} · ${c.label}`, arts, filter: { cen: [r.label], rel: [c.r], ...(startPaper ? { papers: [startPaper] } : {}) } }) });
  const best = base.filter(a => a.m === H.CEN[0] && a.r === 'גבוהה');
  return { read: `${nf(best.length)} כתבות הן גם "נושא הכתבה" וגם בעלות רלוונטיות גבוהה (${pct(best.length, base.length)}% מהבחירה).`, table: { head: ['מרכזיות', ...H.REL], rows: H.CEN.map(c => [c, ...H.REL.map(r => base.filter(a => a.m === c && a.r === r).length)]) } };
});

/* ====== בניית הלשונית ====== */
const ovCards = [];
H.buildOverview = function () {
  const v = $('#view-overview'); v.innerHTML = '';
  v.append(h('div', { class: 'hero' }, h('div', {}, h('h2', {}, 'תמונה היסטורית רחבה'), h('p', {}, 'חמש־עשרה שאלות על הדאטה כולו. כל גרף הוא כניסה אל הכתבות עצמן: לחיצה על עמודה, תא, נקודה או עיגול פותחת מגירה עם הכתבות שמאחוריהן, ומשם אפשר להמשיך לחיפוש או לכתבה. מתחת לכל גרף יש טבלת נתונים והורדה.'))));
  const nav = h('div', { class: 'anav' }, AN.map((a, i) => h('a', { href: 'javascript:void 0', onclick: () => document.getElementById('an' + (i + 1)).scrollIntoView({ behavior: 'smooth' }) }, `${i + 1}. ${a.title}`)));
  v.append(nav);
  const grid = h('div', { class: 'agrid' }); v.append(grid);
  ovCards.length = 0;
  AN.forEach((a, i) => {
    const body = h('div'), read = h('div', { class: 'read hide' }), tbl = h('div', { class: 'tbl hide' });
    let data = null;
    const draw = () => { body.innerHTML = ''; try { data = a.draw(body, draw); } catch (e) { console.error(a.title, e); body.append(h('p', { class: 'muted' }, 'שגיאה בהצגת הגרף')); } read.classList.toggle('hide', !(data && data.read)); read.textContent = data && data.read || ''; tbl.innerHTML = ''; if (data && data.table) { tbl.append(h('table', {}, h('thead', {}, h('tr', {}, data.table.head.map(x => h('th', {}, x)))), h('tbody', {}, data.table.rows.map(r => h('tr', {}, r.map(c => h('td', {}, String(c)))))))); } };
    const card = h('section', { class: 'acard' + (a.wide ? ' wide' : ''), id: 'an' + (i + 1) },
      h('div', { class: 'q' }, h('span', { class: 'num' }, i + 1), h('h3', {}, a.title)), h('p', { class: 'how' }, a.how), body, read,
      h('div', { class: 'foot' }, h('button', { class: 'btn sm', onclick: () => tbl.classList.toggle('hide') }, 'טבלת נתונים'), h('button', { class: 'btn sm', onclick: () => data && data.table && H.download(`analysis-${i + 1}.csv`, H.toCSV(data.table.head, data.table.rows)) }, 'הורדת CSV')), tbl);
    grid.append(card); ovCards.push({ draw });
  });
  // רינדור אחרי שהלשונית גלויה
  requestAnimationFrame(() => ovCards.forEach(c => c.draw()));
};
H.relayoutOverview = () => ovCards.forEach(c => c.draw());
