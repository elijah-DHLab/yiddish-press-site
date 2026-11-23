'use strict';
/* ====== ממשק: כרטיסים, מגירה, חלון כתבה, חיפוש, ציר זמן, ישויות ====== */
const UI = { tab: 'search', F: null, shown: 30, sort: 'dateAsc', yid: false, tl: null, ent: { type: 'pl', sel: null, q: '', shown: 120 }, listCtx: [], listIdx: 0 };

/* ---------- כרטיס כתבה ---------- */
H.card = function (a, o = {}) {
  const tk = o.tokens || [];
  const relCls = { 'גבוהה': 'hi', 'בינונית': 'mid', 'נמוכה': 'lo' }[a.r] || '';
  const c = h('article', { class: 'card' + (o.compact ? ' compact' : ''), style: { '--pc': H.pcol(a.p) }, tabindex: 0, role: 'button', 'aria-label': 'פתיחת כתבה ' + a.id });
  c.append(h('div', { class: 'hd' },
    h('span', { class: 'pbadge' }, H.pname(a.p)), h('time', {}, fmtDate(a.d)),
    a.g && h('span', { class: 'tag' }, a.g), a.m && h('span', { class: 'tag' }, a.m),
    a.r && h('span', { class: 'tag ' + relCls }, 'רלוונטיות ' + a.r),
    a.im.length ? h('span', { class: 'tag' }, '▣ ' + a.im.length) : null));
  c.append(h('p', { class: 'sum', html: highlight(a.s, tk) }));
  if (!o.compact && a.c) c.append(h('p', { class: 'ctx', html: highlight(a.c, tk) }));
  if (!o.compact && a.top.length) {
    const ch = h('div', { class: 'chips' });
    a.top.slice(0, 4).forEach(([t]) => ch.append(h('button', { class: 'chip t-top', title: 'סינון לפי נושא זה', onclick: e => { e.stopPropagation(); H.addEnt('top', H.nk(t)); } }, t)));
    c.append(ch);
  }
  c.addEventListener('click', () => H.openArticle(a, o.list));
  c.addEventListener('keydown', e => { if (e.key === 'Enter') H.openArticle(a, o.list); });
  return c;
};

/* ---------- מגירת נתונים ---------- */
H.openList = function (o) {
  const d = $('#drawer'), body = $('.body', d);
  let arts = [...o.arts].sort(H.sorters[UI.dsort || 'dateAsc']), shown = 40;
  const render = () => {
    arts.sort(H.sorters[UI.dsort || 'dateAsc']);
    body.innerHTML = '';
    body.append(...arts.slice(0, shown).map(a => H.card(a, { compact: true, list: arts, tokens: o.tokens })));
    if (arts.length > shown) body.append(h('button', { class: 'btn more', onclick: () => { shown += 40; render(); } }, `הצג עוד (${nf(arts.length - shown)})`));
    if (!arts.length) body.append(h('p', { class: 'muted' }, 'אין כתבות.'));
  };
  $('.dh h3', d).textContent = o.title; $('.dh .sub', d).textContent = `${nf(arts.length)} כתבות` + (o.sub ? ' · ' + o.sub : '');
  const tools = $('.tools', d); tools.innerHTML = '';
  const sel = h('select', { 'aria-label': 'מיון', onchange: e => { UI.dsort = e.target.value; render(); } },
    h('option', { value: 'dateAsc' }, 'מהישן לחדש'), h('option', { value: 'dateDesc' }, 'מהחדש לישן'), h('option', { value: 'relDesc' }, 'לפי רלוונטיות'));
  sel.value = UI.dsort || 'dateAsc'; tools.append(sel);
  if (o.filter) tools.append(h('button', { class: 'btn sm pri', onclick: () => { H.closeDrawer(); H.applyFilter(o.filter); } }, 'פתח בחיפוש ←'));
  tools.append(h('button', { class: 'btn sm', onclick: () => H.artsCSV(arts, 'selection') }, 'הורד CSV'));
  render();
  d.classList.add('on'); $('#scrim').classList.add('on'); body.scrollTop = 0;
};
H.closeDrawer = () => { $('#drawer').classList.remove('on'); if (!$('#modal').classList.contains('on')) $('#scrim').classList.remove('on'); };

/* ---------- חלון כתבה ---------- */
H.openArticle = function (a, list) {
  UI.listCtx = list && list.length ? list : [a]; UI.listIdx = Math.max(0, UI.listCtx.indexOf(a));
  const m = $('#modal'); m.classList.add('on'); $('#scrim').classList.add('on'); $('#scrim').style.zIndex = 65;
  history.replaceState(null, '', '#a/' + a.id);
  renderArticle(a);
};
H.closeArticle = () => {
  $('#modal').classList.remove('on');
  if (!$('#drawer').classList.contains('on')) $('#scrim').classList.remove('on');
  $('#scrim').style.zIndex = '';
  history.replaceState(null, '', '#' + UI.tab);
};
function stepArticle(d) {
  const i = UI.listIdx + d; if (i < 0 || i >= UI.listCtx.length) return;
  UI.listIdx = i; renderArticle(UI.listCtx[i]); history.replaceState(null, '', '#a/' + UI.listCtx[i].id);
  $('#modal').scrollTop = 0;
}
function entChips(a, t) {
  if (!a[t].length) return null;
  return h('div', { class: 'etype' }, h('b', {}, H.TYPES[t]),
    h('div', { class: 'chips' }, a[t].map(([n, y], i) => h('button', { class: 'chip t-' + t, title: (y ? 'ביידיש: ' + y + ' · ' : '') + 'סינון לפי ' + H.TYPE1[t], onclick: () => { H.closeArticle(); H.addEnt(t, H.nk(n)); } }, n, UI.yid && y ? h('span', { class: 'muted', style: { fontFamily: 'var(--serif)' } }, '‏' + y) : null))));
}
function renderArticle(a) {
  const tk = toks(UI.F.q), box = $('#modal .sheet');
  const L = UI.listCtx, i = UI.listIdx;
  box.innerHTML = '';
  const nli = a.u || ('https://www.nli.org.il/he/newspapers/?a=d&d=' + a.id);
  box.append(h('div', { class: 'mh' },
    h('span', { class: 'pbadge', style: { '--pc': H.pcol(a.p) } }, H.pname(a.p)), h('strong', {}, fmtDate(a.d)),
    h('span', { class: 'muted small', dir: 'ltr' }, a.id), h('span', { class: 'sp' }),
    L.length > 1 ? h('span', { class: 'nav2' }, h('button', { class: 'btn sm', disabled: i === 0, onclick: () => stepArticle(-1), 'aria-label': 'הקודמת' }, '→'), h('span', { class: 'muted small', style: { alignSelf: 'center' } }, `${i + 1}/${L.length}`), h('button', { class: 'btn sm', disabled: i === L.length - 1, onclick: () => stepArticle(1), 'aria-label': 'הבאה' }, '←')) : null,
    h('label', { class: 'small', style: { display: 'flex', gap: '5px', alignItems: 'center' } }, h('input', { type: 'checkbox', checked: UI.yid, onchange: e => { UI.yid = e.target.checked; renderArticle(a); } }), 'כתיב יידי בשמות'),
    h('button', { class: 'x', onclick: H.closeArticle, 'aria-label': 'סגירה' }, '×')));
  const left = h('div'), right = h('div');
  left.append(h('div', { class: 'chips', style: { marginBottom: '10px' } }, [a.g, a.m, a.r && 'רלוונטיות ' + a.r, H.themeName[a.pt]].filter(Boolean).map(x => h('span', { class: 'tag' }, x))));
  left.append(h('h4', {}, 'סיכום'), h('p', { class: 'sumtxt', html: highlight(a.s, tk) }));
  if (a.c) left.append(h('h4', {}, 'מה נאמר על מונח החיפוש'), h('p', { class: 'ctxtxt', html: highlight(a.c, tk) }));
  left.append(h('h4', {}, 'מונחי החיפוש של האיסוף'), h('div', { class: 'chips' }, a.t.map(x => h('span', { class: 'chip' }, x))));
  for (const t of ['top', 'ppl', 'pl', 'org', 'grp']) { const c = entChips(a, t); if (c) left.append(c); }
  // תמונות
  right.append(h('h4', {}, 'מקור'));
  right.append(h('div', { class: 'chips' },
    h('a', { class: 'btn pri', href: nli, target: '_blank', rel: 'noopener' }, 'פתיחה בספרייה הלאומית ↗'),
    h('button', { class: 'btn', onclick: e => copy(`${H.pname(a.p)}, ${fmtDate(a.d)}. הספרייה הלאומית, עיתונות יהודית היסטורית, מזהה ${a.id}. ${nli}`, e.target, 'הציטוט הועתק') }, 'העתק ציטוט'),
    h('button', { class: 'btn', onclick: e => copy(location.href.split('#')[0] + '#a/' + a.id, e.target, 'הקישור הועתק') }, 'קישור לכתבה')));
  right.append(h('h4', {}, a.im.length ? `תמונות הכתבה (${a.im.length} חלקים)` : 'תמונות'));
  if (a.im.length) {
    const gal = h('div', { class: 'gallery' });
    a.im.forEach((id, k) => {
      const link = h('a', { href: 'https://drive.google.com/file/d/' + id + '/view', target: '_blank', rel: 'noopener', title: 'חלק ' + (k + 1) });
      const img = h('img', { loading: 'lazy', alt: 'חלק ' + (k + 1) + ' של הכתבה', src: 'https://drive.google.com/thumbnail?id=' + id + '&sz=w500' });
      img.addEventListener('error', () => { img.replaceWith(h('div', { class: 'fallback' }, 'חלק ' + (k + 1) + ' · פתיחה בכונן')); });
      link.append(img, h('span', { class: 'pn' }, k + 1));
      link.addEventListener('click', e => { if (e.ctrlKey || e.metaKey || e.shiftKey) return; e.preventDefault(); lightbox(a.im, k); });
      gal.append(link);
    });
    right.append(gal, h('p', { class: 'small muted', style: { marginTop: '6px' } }, 'התמונות נטענות מתיקיית הכונן של המעבדה. לחיצה מגדילה; תמיד אפשר לפתוח את העמוד המקורי בספרייה הלאומית.'));
  } else right.append(h('p', { class: 'small muted' }, 'לכתבה זו אין תיקיית תמונות בכונן. אפשר לראות את העמוד המקורי דרך הקישור לספרייה הלאומית.'));
  // OCR
  const det = h('details', { style: { marginTop: '18px' } }, h('summary', {}, 'טקסט ביידיש (OCR מתוקן)'));
  const yb = h('div', { class: 'yid', lang: 'yi', dir: 'rtl' }, 'טוען…'); det.append(yb);
  let loaded = false;
  det.addEventListener('toggle', async () => {
    if (!det.open || loaded) return; loaded = true;
    try { const o = await H.loadOCR(); const t = o[a.id] || '(אין טקסט)'; yb.innerHTML = highlight(t, UI.F.scope === 'ocr' ? tk : []); }
    catch (e) { yb.textContent = 'לא ניתן לטעון את ocr.json'; }
  });
  if (UI.F.scope === 'ocr' && tk.length) det.open = true;
  right.append(det);
  box.append(h('div', { class: 'mb' }, left, right));
}
function copy(text, btn, msg) {
  const done = () => { const o = btn.textContent; btn.textContent = msg; setTimeout(() => btn.textContent = o, 1400); };
  (navigator.clipboard ? navigator.clipboard.writeText(text) : Promise.reject()).then(done, () => { const t = h('textarea'); t.value = text; document.body.append(t); t.select(); try { document.execCommand('copy'); done(); } catch (e) { } t.remove(); });
}
function lightbox(ids, k) {
  const lb = $('#lightbox'); let i = k;
  const draw = () => { lb.innerHTML = ''; lb.append(h('img', { src: 'https://drive.google.com/thumbnail?id=' + ids[i] + '&sz=w2000', alt: 'חלק ' + (i + 1) }),
    h('div', { class: 'bar' }, h('button', { class: 'btn', onclick: e => { e.stopPropagation(); i = (i + 1) % ids.length; draw(); } }, '→ הבא'), h('span', {}, `${i + 1} / ${ids.length}`), h('button', { class: 'btn', onclick: e => { e.stopPropagation(); i = (i - 1 + ids.length) % ids.length; draw(); } }, 'הקודם ←'),
      h('a', { class: 'btn', href: 'https://drive.google.com/file/d/' + ids[i] + '/view', target: '_blank', rel: 'noopener', onclick: e => e.stopPropagation() }, 'פתח בכונן ↗'), h('button', { class: 'btn', onclick: () => lb.classList.remove('on') }, 'סגירה'))); };
  draw(); lb.classList.add('on');
}

/* ---------- הצעות חיפוש (ישויות + נושאי-על) ---------- */
H.suggest = function (q, type, limit = 9) {
  const n = norm(q); if (!n) return [];
  const types = type && H.TYPES[type] ? [type] : Object.keys(H.TYPES);
  const out = [];
  for (const t of types) for (const e of H.idx[t].values()) {
    const pos = e._n.indexOf(n); if (pos < 0) continue;
    out.push({ kind: 'ent', type: t, key: e.key, h: e.h, y: e.y[0] || '', count: e.count, score: (pos === 0 ? 1000 : 0) + (e._n.startsWith(n) ? 500 : 0) + e.count - e.h.length * .1 });
  }
  if (!type || type === 'all') for (const t of H.meta.themes) if (norm(t.h).includes(n)) out.push({ kind: 'theme', key: t.k, h: t.h, y: '', count: H.A.filter(a => a.th.includes(t.k)).length, score: 900 });
  return out.sort((a, b) => b.score - a.score).slice(0, limit);
};
H.attachSuggest = function (input, getType, onPick, host) {
  let box = null, act = -1, items = [];
  const close = () => { if (box) { box.remove(); box = null; } act = -1; };
  const draw = () => {
    close(); const q = input.value; if (!q.trim()) return;
    items = H.suggest(q, getType()); if (!items.length) return;
    box = h('div', { class: 'suggest', role: 'listbox' }, items.map((it, i) => h('button', { type: 'button', role: 'option', onmousedown: e => { e.preventDefault(); pick(i); } },
      h('span', { class: 'tp' }, it.kind === 'theme' ? 'נושא-על' : H.TYPE1[it.type]), h('span', {}, it.h), it.y ? h('span', { class: 'y' }, it.y) : null, h('span', { class: 'c' }, nf(it.count)))));
    host.append(box);
  };
  const pick = i => { const it = items[i]; close(); onPick(it); };
  input.addEventListener('input', draw);
  input.addEventListener('blur', () => setTimeout(close, 120));
  input.addEventListener('keydown', e => {
    if (!box) return;
    const bs = $$('button', box);
    if (e.key === 'ArrowDown') { e.preventDefault(); act = (act + 1) % bs.length; }
    else if (e.key === 'ArrowUp') { e.preventDefault(); act = (act - 1 + bs.length) % bs.length; }
    else if (e.key === 'Enter' && act >= 0) { e.preventDefault(); e.stopImmediatePropagation(); pick(act); return; }
    else if (e.key === 'Escape') { close(); return; } else return;
    bs.forEach((b, i) => b.classList.toggle('act', i === act));
  });
};

/* ---------- פעולות סינון משותפות ---------- */
H.addEnt = function (type, key) {
  const F = UI.F; if (!F.ents.some(e => e.type === type && e.key === key)) F.ents.push({ type, key });
  H.showTab('search'); renderSearch();
};
H.applyFilter = function (spec) { // פותח את לשונית החיפוש עם סינון חלקי
  const F = H.newF();
  if (spec.papers) F.papers = new Set(spec.papers);
  for (const k of ['q', 'scope', 'mode', 'from', 'to', 'pt', 'th', 'jw']) if (spec[k] != null) F[k] = spec[k];
  for (const k of ['genre', 'cen', 'rel']) if (spec[k]) F[k] = new Set(spec[k]);
  if (spec.ents) F.ents = spec.ents.map(e => ({ ...e }));
  UI.F = F; syncSearchControls(); H.showTab('search'); renderSearch();
};
const entLabel = e => { const x = H.entity(e.type, e.key); return (H.TYPE1[e.type]) + ': ' + (x ? x.h : e.key); };

/* ---------- לשונית חיפוש ---------- */
const SCOPES = [['all', 'הכול'], ['sum', 'סיכום והקשר'], ['top', 'נושאים'], ['ppl', 'אנשים'], ['pl', 'מקומות'], ['org', 'ארגונים'], ['grp', 'קבוצות'], ['ocr', 'טקסט ביידיש']];
function buildSearch() {
  const v = $('#view-search');
  v.innerHTML = '';
  v.append(h('div', { class: 'hero' },
    h('div', {}, h('h2', {}, 'חיפוש בארכיון'), h('p', {}, 'חיפוש חופשי בעברית או ביידיש, או בחירה של נושא, אדם, מקום, ארגון וקבוצת אוכלוסייה מתוך הרשימה. כל תוצאה מקושרת לסיכום, לישויות, לתמונות העמוד ולספרייה הלאומית.')),
    h('div', { class: 'stats', id: 'stats' })));
  const side = h('aside', { class: 'side', id: 'side', 'aria-label': 'מסננים' });
  const main = h('div', {});
  v.append(h('div', { class: 'layout' }, side, main));

  // סרגל חיפוש
  const scope = h('select', { id: 'scope', 'aria-label': 'היכן לחפש', onchange: e => { UI.F.scope = e.target.value; renderSearch(); } }, SCOPES.map(([k, l]) => h('option', { value: k }, l)));
  const q = h('input', { id: 'q', type: 'search', placeholder: 'סלוניקי, אגאדיר, חינוך עברי, פוגרום…', 'aria-label': 'מילות חיפוש', autocomplete: 'off' });
  const mode = h('select', { id: 'mode', 'aria-label': 'אופן התאמה', onchange: e => { UI.F.mode = e.target.value; renderSearch(); } }, h('option', { value: 'all' }, 'כל המילים'), h('option', { value: 'any' }, 'אחת המילים'), h('option', { value: 'phrase' }, 'ביטוי מדויק'));
  const sr = h('div', { class: 'searchrow' }, scope, q, mode);
  main.append(sr);
  main.append(h('p', { class: 'small muted', style: { margin: '6px 4px 0' } }, 'הקלידו שם והמערכת תציע ישויות מדויקות (בחירה = מסנן). Enter = חיפוש טקסט חופשי. הכתיב היידי מנורמל: ײַ=יי, װ=וו, ללא ניקוד, וללא הבדל בין אותיות סופיות.'));
  let deb; q.addEventListener('input', () => { clearTimeout(deb); deb = setTimeout(() => { UI.F.q = q.value; renderSearch(); }, 220); });
  q.addEventListener('keydown', e => { if (e.key === 'Enter') { clearTimeout(deb); UI.F.q = q.value; renderSearch(); } });
  H.attachSuggest(q, () => UI.F.scope, it => { q.value = ''; UI.F.q = ''; if (it.kind === 'theme') UI.F.th = it.key; else if (!UI.F.ents.some(e => e.type === it.type && e.key === it.key)) UI.F.ents.push({ type: it.type, key: it.key }); renderSearch(); }, sr);
  main.append(h('div', { class: 'activebar', id: 'activebar' }));
  main.append(h('div', { class: 'mini' }, h('div', { class: 'cap' }, h('span', {}, 'התפלגות התוצאות בזמן — גררו על הציר כדי לצמצם תקופה'), h('span', { id: 'rangecap' })), h('div', { id: 'mini' })));
  main.append(h('div', { class: 'resbar' }, h('div', {}, h('strong', { id: 'rescount', role: 'status', 'aria-live': 'polite' }), h('div', { class: 'small muted', id: 'resdetail' })),
    h('div', { class: 'acts' },
      h('select', { id: 'sort', 'aria-label': 'מיון', onchange: e => { UI.sort = e.target.value; UI.shown = 30; renderSearch(); } }, h('option', { value: 'dateAsc' }, 'מהישן לחדש'), h('option', { value: 'dateDesc' }, 'מהחדש לישן'), h('option', { value: 'relDesc' }, 'לפי רלוונטיות ומרכזיות')),
      h('button', { class: 'btn', id: 'togSide', style: { display: 'none' }, onclick: () => $('#side').classList.toggle('hide') }, 'מסננים'),
      h('button', { class: 'btn', onclick: () => H.artsCSV(UI.res, 'search-results') }, 'הורדת התוצאות (CSV)'))));
  main.append(h('div', { id: 'results' }), h('button', { class: 'btn more hide', id: 'moreBtn', onclick: () => { UI.shown += 30; renderResults(); } }, 'הצג עוד'));
  buildSide();
}
function buildSide() {
  const s = $('#side'); s.innerHTML = '';
  s.append(h('div', { class: 'head' }, h('strong', {}, 'מסננים'), h('button', { class: 'btn sm', onclick: () => { UI.F = H.newF(); syncSearchControls(); renderSearch(); } }, 'איפוס הכול')));
  const facet = (title, id, field, values, labelFn) => {
    s.append(h('h3', {}, title));
    const box = h('div', { id: 'f-' + id });
    for (const v of values) box.append(h('label', { class: 'fopt', 'data-v': v }, h('input', { type: 'checkbox', 'data-f': id, value: v, onchange: onFacet }), labelFn ? labelFn(v) : v, h('span', { class: 'n' })));
    s.append(box);
  };
  s.append(h('h3', {}, 'עיתון'));
  const pb = h('div', { id: 'f-paper' });
  for (const p of H.paperKeys) pb.append(h('label', { class: 'fopt', 'data-v': p }, h('input', { type: 'checkbox', 'data-f': 'paper', value: p, checked: true, onchange: onFacet }), h('i', { class: 'dot', style: { background: H.pcol(p) } }), H.pname(p), h('span', { class: 'n' })));
  s.append(pb);
  s.append(h('h3', {}, 'תקופה'), h('div', { class: 'two' },
    h('input', { type: 'date', id: 'from', 'aria-label': 'מתאריך', min: H.minD, max: H.maxD, onchange: e => { UI.F.from = e.target.value; renderSearch(); } }),
    h('input', { type: 'date', id: 'to', 'aria-label': 'עד תאריך', min: H.minD, max: H.maxD, onchange: e => { UI.F.to = e.target.value; renderSearch(); } })));
  const cnt = {}; for (const a of H.A) cnt[a.g] = (cnt[a.g] || 0) + 1;
  facet('סוגה', 'genre', 'g', Object.keys(cnt).filter(Boolean).sort((a, b) => cnt[b] - cnt[a]));
  facet('מרכזיות המונח בכתבה', 'cen', 'm', H.CEN.filter(c => H.A.some(a => a.m === c)));
  facet('רלוונטיות למחקר', 'rel', 'r', H.REL.filter(c => H.A.some(a => a.r === c)));
  s.append(h('h3', {}, 'נושא-על (קיבוץ אוטומטי)'));
  const ts = h('select', { id: 'f-th', 'aria-label': 'נושא-על', onchange: e => { UI.F.th = e.target.value; renderSearch(); } }, h('option', { value: '' }, 'כל הנושאים'), H.meta.themes.map(t => h('option', { value: t.k }, t.h)));
  s.append(ts, h('p', { class: 'small muted', style: { marginTop: '6px' } }, 'תיוג לפי מילות מפתח בשדה "נושאים". כלי גלישה, לא קטגוריה מחקרית. הכללים בלשונית "על הנתונים".'));
}
function onFacet(e) {
  const f = e.target.dataset.f, v = e.target.value, F = UI.F, set = f === 'paper' ? F.papers : F[f];
  e.target.checked ? set.add(v) : set.delete(v);
  UI.shown = 30; renderSearch();
}
function syncSearchControls() {
  const F = UI.F;
  $('#q').value = F.q; $('#scope').value = F.scope; $('#mode').value = F.mode; $('#from').value = F.from; $('#to').value = F.to; $('#f-th').value = F.th;
  $$('#side input[type=checkbox]').forEach(c => { const f = c.dataset.f; c.checked = f === 'paper' ? F.papers.has(c.value) : F[f].has(c.value); });
  $('#sort').value = UI.sort;
}
function updateFacets() {
  const F = UI.F;
  const upd = (id, field, skip, multi) => {
    const arts = H.filter(F, skip), c = {};
    for (const a of arts) { const vals = multi ? a[field] : [a[field]]; for (const v of vals) c[v] = (c[v] || 0) + 1; }
    $$('#f-' + id + ' .fopt').forEach(l => { const n = c[l.dataset.v] || 0; $('.n', l).textContent = nf(n); l.classList.toggle('zero', !n); });
  };
  upd('paper', 'p', 'paper'); upd('genre', 'g', 'genre'); upd('cen', 'm', 'cen'); upd('rel', 'r', 'rel');
  const arts = H.filter(F, 'th'), c = {}; for (const a of arts) for (const t of a.th) c[t] = (c[t] || 0) + 1;
  $$('#f-th option').forEach(o => { if (!o.value) return; o.textContent = H.themeName[o.value] + ` (${nf(c[o.value] || 0)})`; });
}
async function renderSearch() {
  const F = UI.F;
  if (F.scope === 'ocr' && toks(F.q).length && !H.ocrN) {
    $('#rescount').textContent = 'מכין אינדקס של הטקסט ביידיש… (פעם אחת, כמה שניות)';
    try { await H.ensureOcrNorm(p => { $('#resdetail').textContent = Math.round(p * 100) + '%'; }); } catch (e) { $('#rescount').textContent = 'שגיאה בטעינת ocr.json'; return; }
  }
  UI.res = H.filter(F).sort(H.sorters[UI.sort]);
  updateFacets(); renderActive(); renderMini(); renderResults(true);
  $('#rescount').textContent = `${nf(UI.res.length)} כתבות` + (UI.res.length !== H.A.length ? ` מתוך ${nf(H.A.length)}` : '');
  const byP = H.paperKeys.map(p => `${H.pname(p)}: ${nf(UI.res.filter(a => a.p === p).length)}`).join(' · ');
  $('#resdetail').textContent = byP;
}
function renderActive() {
  const F = UI.F, bar = $('#activebar'); bar.innerHTML = '';
  const add = (label, fn) => bar.append(h('span', { class: 'chip f' }, label, h('button', { 'aria-label': 'הסרה', onclick: () => { fn(); syncSearchControls(); renderSearch(); } }, '×')));
  if (toks(F.q).length) add(`טקסט: ${F.q}`, () => F.q = '');
  F.ents.forEach((e, i) => add(entLabel(e), () => F.ents.splice(i, 1)));
  if (F.th) add('נושא-על: ' + H.themeName[F.th], () => F.th = '');
  if (F.pt) add('נושא ראשי: ' + H.themeName[F.pt], () => F.pt = '');
  if (F.jw) add('הקשר יהודי (היוריסטי)', () => F.jw = 0);
  if (F.from || F.to) add(`תקופה: ${F.from ? fmtDate(F.from) : '…'} – ${F.to ? fmtDate(F.to) : '…'}`, () => { F.from = ''; F.to = ''; });
  $('#rangecap').innerHTML = (F.from || F.to) ? ltr(`${F.from || H.minD} → ${F.to || H.maxD}`) : '';
}
function renderMini() {
  const F2 = { ...UI.F, from: '', to: '' }, arts = H.filter(F2), host = $('#mini');
  const buckets = allBuckets('month'), idx = new Map(buckets.map((k, i) => [k, i]));
  const cell = buckets.map(() => ({}));
  for (const a of arts) { const i = idx.get(a.d.slice(0, 7)); if (i != null) (cell[i][a.p] = cell[i][a.p] || []).push(a); }
  const series = H.paperKeys.map(p => ({ key: p, label: H.pname(p), color: H.pcol(p) }));
  const B = H.timeBars(host, { buckets, series, gran: 'month', height: 54, aria: 'התפלגות בזמן', cell: (bi, si) => cell[bi][series[si].key] || [] });
  const svg = B.svg; const sel = S('rect', { y: B.m.t, height: B.Ht, fill: '#00a9d4', 'fill-opacity': .22, stroke: '#00a9d4', style: 'pointer-events:none' }); svg.append(sel);
  const showSel = (i0, i1) => { sel.setAttribute('x', B.m.l + Math.min(i0, i1) * B.bw); sel.setAttribute('width', (Math.abs(i1 - i0) + 1) * B.bw); sel.style.display = ''; };
  sel.style.display = 'none';
  if (UI.F.from || UI.F.to) {
    const f = UI.F.from ? buckets.findIndex(k => k >= UI.F.from.slice(0, 7)) : 0; let t = UI.F.to ? buckets.map(k => k <= UI.F.to.slice(0, 7)).lastIndexOf(true) : buckets.length - 1;
    if (f >= 0 && t >= f) showSel(f, t);
  }
  const ix = e => { const r = svg.getBoundingClientRect(); const x = (e.clientX - r.left) * (B.W / r.width); return Math.max(0, Math.min(buckets.length - 1, Math.floor((x - B.m.l) / B.bw))); };
  let start = null;
  svg.addEventListener('pointerdown', e => { start = ix(e); svg.setPointerCapture(e.pointerId); showSel(start, start); });
  svg.addEventListener('pointermove', e => { if (start != null) showSel(start, ix(e)); });
  svg.addEventListener('pointerup', e => {
    if (start == null) return; const end = ix(e), a = Math.min(start, end), b = Math.max(start, end); start = null;
    UI.F.from = buckets[a] + '-01'; UI.F.to = monthEnd(buckets[b]); syncSearchControls(); renderSearch();
  });
}
function renderResults(reset) {
  const res = UI.res, box = $('#results'); if (reset) { UI.shown = 30; box.innerHTML = ''; }
  const tk = UI.F.scope === 'ocr' ? [] : toks(UI.F.q);
  const from = reset ? 0 : box.children.length;
  box.append(...res.slice(from, UI.shown).map(a => H.card(a, { tokens: tk, list: res })));
  if (!res.length) box.append(h('div', { class: 'panel muted' }, 'לא נמצאו כתבות. נסו להסיר מסנן, להרחיב את התקופה או לשנות את אופן ההתאמה.'));
  $('#moreBtn').classList.toggle('hide', res.length <= UI.shown);
  $('#moreBtn').textContent = `הצג עוד (${nf(res.length - UI.shown)})`;
}
function renderStats() {
  const c = Object.keys(H.TYPES).map(t => H.idx[t].size);
  $('#stats').innerHTML = `<div class="stat"><strong>${nf(H.A.length)}</strong><span>כתבות מנותחות</span></div><div class="stat"><strong>${H.paperKeys.length}</strong><span>עיתונים</span></div><div class="stat"><strong>${ltr(H.minD.slice(0, 4) + '–' + H.maxD.slice(0, 4))}</strong><span>טווח שנים</span></div><div class="stat"><strong>${nf(H.idx.pl.size + H.idx.ppl.size + H.idx.org.size)}</strong><span>מקומות, אישים וארגונים</span></div>`;
}

/* ---------- לשונית ציר זמן והשוואה ---------- */
H.subjPred = s => {
  if (s.kind === 'ent') return a => a['k_' + s.type].includes(s.key);
  if (s.kind === 'theme') return a => a.th.includes(s.key);
  if (s.kind === 'pt') return a => a.pt === s.key;
  if (s.kind === 'jw') return a => !!a.jw;
  const t = toks(s.q); return a => t.length && t.every(x => a._all.includes(x));
};
H.subjLabel = s => s.kind === 'ent' ? entLabel(s) : s.kind === 'theme' ? 'נושא-על: ' + H.themeName[s.key] : s.kind === 'pt' ? 'נושא ראשי: ' + H.themeName[s.key] : s.kind === 'jw' ? 'הקשר יהודי (היוריסטי)' : 'טקסט: ' + s.q;
H.subjFilter = s => s.kind === 'ent' ? { ents: [{ type: s.type, key: s.key }] } : s.kind === 'theme' ? { th: s.key } : s.kind === 'pt' ? { pt: s.key } : s.kind === 'jw' ? { jw: 1 } : { q: s.q };

function buildTimeline() {
  const v = $('#view-timeline'); v.innerHTML = '';
  UI.tl = UI.tl || { subj: { kind: 'ent', type: 'pl', key: 'מרוקו' }, gran: 'quarter', measure: 'count', view: 'lanes', events: true, papers: new Set(H.paperKeys), sel: null, shown: 25 };
  v.append(h('div', { class: 'hero' }, h('div', {}, h('h2', {}, 'ציר זמן והשוואה בין עיתונים'), h('p', {}, 'בחרו נושא, אדם, מקום, ארגון או קבוצה, וראו מתי כל עיתון עסק בהם. לחיצה על עמודה בוחרת תקופה, ומתחת מוצגות הכתבות של העיתונים זו לצד זו לאותה תקופה.'))));
  const T = UI.tl;
  const inp = h('input', { type: 'text', id: 'tlq', placeholder: 'חיפשו נושא, מקום, אדם, ארגון… (או טקסט חופשי עם Enter)', autocomplete: 'off', 'aria-label': 'נושא להשוואה' });
  const wrap = h('div', { style: { position: 'relative' } }, inp);
  const mk = (name, opts, key) => h('div', {}, h('label', {}, name), h('div', { class: 'seg', role: 'group' }, opts.map(([k, l]) => h('button', { type: 'button', class: T[key] === k ? 'on' : '', onclick: () => { T[key] = k; if (key === 'measure' && k === 'share') T.view = 'lines'; if (key === 'view' && k === 'lanes') T.measure = 'count'; T.sel = null; buildTimeline(); } }, l))));
  v.append(h('div', { class: 'panel' }, h('div', { class: 'ctrl' },
    h('div', {}, h('label', {}, 'נושא להשוואה'), wrap),
    mk('פירוט זמן', [['month', 'חודש'], ['quarter', 'רבעון'], ['year', 'שנה']], 'gran'),
    mk('מדד', [['count', 'מספר כתבות'], ['share', '% מהדגימה']], 'measure'),
    mk('תצוגה', [['lanes', 'נתיבים'], ['lines', 'קווים']], 'view')),
    h('div', { class: 'chips', id: 'tlsubj', style: { marginTop: '12px', alignItems: 'center' } }),
    h('div', { style: { display: 'flex', gap: '16px', flexWrap: 'wrap', marginTop: '10px', alignItems: 'center' } },
      H.paperKeys.map(p => h('label', { class: 'fopt' }, h('input', { type: 'checkbox', checked: T.papers.has(p), onchange: e => { e.target.checked ? T.papers.add(p) : T.papers.delete(p); drawTL(); } }), h('i', { class: 'dot', style: { background: H.pcol(p) } }), H.pname(p))),
      h('label', { class: 'fopt' }, h('input', { type: 'checkbox', checked: T.events, onchange: e => { T.events = e.target.checked; drawTL(); } }), 'אירועי רקע'))));
  v.append(h('div', { class: 'panel tlchart', id: 'tlchart', style: { marginTop: '16px' } }), h('div', { id: 'tlnote' }), h('div', { id: 'tlcols' }));
  H.attachSuggest(inp, () => 'all', it => { inp.value = ''; T.subj = it.kind === 'theme' ? { kind: 'theme', key: it.key } : { kind: 'ent', type: it.type, key: it.key }; T.sel = null; drawTL(); }, wrap);
  inp.addEventListener('keydown', e => { if (e.key === 'Enter' && inp.value.trim()) { T.subj = { kind: 'text', q: inp.value.trim() }; T.sel = null; inp.value = ''; drawTL(); } });
  drawTL();
}
function drawTL() {
  const T = UI.tl, pred = H.subjPred(T.subj), papers = H.paperKeys.filter(p => T.papers.has(p));
  const chips = $('#tlsubj'); chips.innerHTML = '';
  chips.append(h('span', { class: 'chip f' }, H.subjLabel(T.subj)), h('button', { class: 'btn sm', onclick: () => H.applyFilter(H.subjFilter(T.subj)) }, 'פתח בחיפוש'));
  const buckets = allBuckets(T.gran), idx = new Map(buckets.map((k, i) => [k, i]));
  const hit = H.A.filter(a => T.papers.has(a.p) && pred(a));
  const per = {}; for (const p of papers) per[p] = buckets.map(() => []);
  for (const a of hit) { const i = idx.get(bucketKey(a.d, T.gran)); if (i != null) per[a.p][i].push(a); }
  const allP = {}; for (const p of papers) allP[p] = buckets.map(() => 0);
  for (const a of H.A) if (T.papers.has(a.p)) { const i = idx.get(bucketKey(a.d, T.gran)); if (i != null) allP[a.p][i]++; }
  const host = $('#tlchart'); host.innerHTML = '';
  const onSel = (k) => { T.sel = T.sel === k ? null : k; drawTL(); setTimeout(() => $('#tlcols') && $('#tlcols').scrollIntoView({ behavior: 'smooth', block: 'nearest' }), 50); };
  if (!hit.length) host.append(h('p', { class: 'muted' }, 'אין כתבות לנושא זה בעיתונים שנבחרו.'));
  else if (T.view === 'lanes') {
    const ymax = Math.max(1, ...papers.flatMap(p => per[p].map(x => x.length)));
    for (const p of papers) {
      const lane = h('div', { class: 'lane' }, h('div', { class: 'ln' }, h('i', { class: 'dot', style: { background: H.pcol(p) } }), `${H.pname(p)} · ${nf(per[p].flat().length)} כתבות`, h('span', { class: 'muted small', style: { fontWeight: 400 }, html: 'בדגימה: ' + ltr(H.paperRange[p][0].slice(0, 7) + ' – ' + H.paperRange[p][1].slice(0, 7)) })));
      const ch = h('div'); lane.append(ch); host.append(lane);
      H.timeBars(ch, { buckets, gran: T.gran, height: 84, ymax, range: H.paperRange[p], events: T.events && p === papers[0], sel: T.sel, series: [{ key: p, label: H.pname(p), color: H.pcol(p) }], cell: bi => per[p][bi], aria: 'ציר זמן ' + H.pname(p), onClick: (arts, k) => onSel(k) });
    }
  } else {
    const share = T.measure === 'share';
    const inR = (k, p) => { const [f, t] = bucketRange(k); return !(t < H.paperRange[p][0] || f > H.paperRange[p][1]); };
    const series = papers.map(p => ({ key: p, label: H.pname(p), color: H.pcol(p), vals: buckets.map((k, i) => !inR(k, p) ? null : share ? (allP[p][i] ? per[p][i].length / allP[p][i] * 100 : 0) : per[p][i].length) }));
    const ch = h('div'); host.append(ch);
    H.lineChart(ch, { buckets, gran: T.gran, height: 240, series, events: T.events, sel: T.sel, aria: 'השוואת עיתונים', fmt: (v, s, i) => share ? `${Math.round(v * 10) / 10}% (${per[s.key][i].length} מתוך ${allP[s.key][i]})` : nf(v), onClick: (s, i) => onSel(buckets[i]) });
    host.prepend(h('div', { class: 'legend' }, series.map(s => h('span', {}, h('i', { class: 'dot', style: { background: s.color } }), s.label)), share ? h('span', { class: 'muted' }, 'אחוז הכתבות בנושא מתוך כלל הכתבות של העיתון בדגימה באותו פרק זמן. בפרקים עם מעט כתבות האחוזים תנודתיים.') : null));
  }
  const note = $('#tlnote'); note.innerHTML = '';
  note.append(h('div', { class: 'note' }, 'האזורים האפורים בגרף הם תקופות שמחוץ לטווח הכתבות שנאספו מכל עיתון, ולא תקופות שבהן העיתון שתק. ' + 'שימו לב: הדגימה נאספה לפי מונחי חיפוש שונים בכל עיתון (מרוקו/פאס/מראכש בדער פריינד ובהיינט; דמשק וסלוניקי באונזר לעבן). לכן נפח הכתבות הכולל אינו משקף את היקף הכיסוי של העיתון. ההשוואה תקפה בעיקר לנושאים שמופיעים בכמה עיתונות, ולמגמות ולא לסכומים מוחלטים.'));
  // עמודות
  const cols = $('#tlcols'); cols.innerHTML = '';
  const rng = T.sel ? bucketRange(T.sel) : null;
  const info = h('div', { style: { display: 'flex', gap: '10px', alignItems: 'center', marginTop: '18px', flexWrap: 'wrap' } },
    h('strong', {}, T.sel ? 'הכתבות בתקופה: ' + bucketLabel(T.sel) : 'כל הכתבות בנושא, לפי עיתון'),
    T.sel ? h('button', { class: 'btn sm', onclick: () => { T.sel = null; drawTL(); } }, 'נקה בחירה ×') : h('span', { class: 'muted small' }, 'לחצו על עמודה בגרף כדי לבחור תקופה'),
    h('button', { class: 'btn sm', onclick: () => H.artsCSV(hit.filter(a => !rng || (a.d >= rng[0] && a.d <= rng[1])), 'timeline') }, 'הורדת CSV'));
  const grid = h('div', { class: 'cols' });
  for (const p of papers) {
    const list = hit.filter(a => a.p === p && (!rng || (a.d >= rng[0] && a.d <= rng[1]))).sort(H.sorters.dateAsc);
    const col = h('div', { style: { '--pc': H.pcol(p) } }, h('div', { class: 'colh' }, h('i', { class: 'dot', style: { background: H.pcol(p) } }), H.pname(p), h('span', { class: 'muted small' }, nf(list.length) + ' כתבות')));
    list.slice(0, T.shown).forEach(a => col.append(H.card(a, { compact: true, list })));
    if (list.length > T.shown) col.append(h('button', { class: 'btn more', onclick: () => H.openList({ title: `${H.pname(p)} · ${H.subjLabel(T.subj)}`, arts: list, filter: { ...H.subjFilter(T.subj), papers: [p] } }) }, `כל ${nf(list.length)} הכתבות במגירה`));
    if (!list.length) col.append(h('p', { class: 'muted small' }, 'אין כתבות.'));
    grid.append(col);
  }
  cols.append(info, grid);
}

/* ---------- לשונית ישויות ---------- */
function buildEntities() {
  const v = $('#view-entities'); v.innerHTML = '';
  const E = UI.ent;
  v.append(h('div', { class: 'hero' }, h('div', {}, h('h2', {}, 'ישויות'), h('p', {}, 'אנשים, מקומות, ארגונים, קבוצות אוכלוסייה ונושאים, בדירוג לפי מספר הכתבות. בחרו ישות לראות את התפלגותה בין העיתונים ובזמן, ואילו ישויות מופיעות לצידה.'))));
  const tabs = h('div', { class: 'etabs' }, Object.entries(H.TYPES).map(([k, l]) => h('button', { class: E.type === k ? 'on' : '', onclick: () => { E.type = k; E.sel = null; E.shown = 120; buildEntities(); } }, `${l} (${nf(H.idx[k].size)})`)));
  const q = h('input', { type: 'search', placeholder: 'סינון הרשימה: עברית או יידיש…', value: E.q, 'aria-label': 'סינון רשימת ישויות', style: { padding: '9px 12px', border: '1px solid var(--line)', borderRadius: '9px', minWidth: '260px' } });
  q.addEventListener('input', () => { E.q = q.value; E.shown = 120; drawEntTable(); });
  const left = h('div', {}, tabs, h('div', { style: { margin: '0 0 10px' } }, q), h('div', { class: 'panel', style: { padding: 0, overflow: 'hidden' }, id: 'etbl' }));
  const right = h('div', { class: 'detail panel', id: 'edetail' }, h('p', { class: 'muted' }, 'בחרו ישות מהרשימה.'));
  v.append(h('div', { class: 'elayout' }, left, right));
  drawEntTable(); if (E.sel) drawEntDetail();
}
function drawEntTable() {
  const E = UI.ent, n = norm(E.q);
  let list = [...H.idx[E.type].values()].sort((a, b) => b.count - a.count || a.h.localeCompare(b.h, 'he'));
  if (n) list = list.filter(e => e._n.includes(n));
  const host = $('#etbl'); host.innerHTML = '';
  const tb = h('table', { class: 'etable' }, h('thead', {}, h('tr', {}, h('th', {}, 'שם'), h('th', {}, 'כתבות'), h('th', {}, 'עיתונים'), h('th', {}, 'טווח'), h('th', {}, 'לפי שנה'))));
  const body = h('tbody');
  for (const e of list.slice(0, E.shown)) {
    const tr = h('tr', { class: E.sel === e.key ? 'sel' : '', tabindex: 0, onclick: () => { E.sel = e.key; $$('#etbl tr.sel').forEach(x => x.classList.remove('sel')); tr.classList.add('sel'); drawEntDetail(); }, onkeydown: ev => { if (ev.key === 'Enter') tr.click(); } });
    const stk = h('div', { class: 'stk', title: H.paperKeys.map(p => H.pname(p) + ': ' + (e.papers[p] || 0)).join(' · ') }, H.paperKeys.map(p => e.papers[p] ? h('i', { style: { width: (e.papers[p] / e.count * 100) + '%', background: H.pcol(p) } }) : null));
    tr.append(h('td', {}, h('div', {}, e.h), e.y[0] ? h('div', { class: 'y' }, e.y[0]) : null), h('td', {}, nf(e.count)), h('td', {}, stk),
      h('td', { class: 'small muted', html: ltr(e.first.slice(0, 4) === e.last.slice(0, 4) ? e.first.slice(0, 4) : e.first.slice(0, 4) + '–' + e.last.slice(0, 4)) }),
      h('td', { html: H.spark(H.years.map(y => e.byYear[y] || 0)) }));
    body.append(tr);
  }
  tb.append(body); host.append(tb);
  if (list.length > E.shown) host.append(h('button', { class: 'btn more', onclick: () => { E.shown += 150; drawEntTable(); } }, `הצג עוד (${nf(list.length - E.shown)})`));
  if (!list.length) host.append(h('p', { class: 'muted', style: { padding: '14px' } }, 'לא נמצאו ישויות.'));
}
function drawEntDetail() {
  const E = UI.ent, e = H.entity(E.type, E.sel), box = $('#edetail'); if (!e) return;
  box.innerHTML = '';
  box.append(h('div', { class: 'chips', style: { marginBottom: '6px' } }, h('span', { class: 'tag' }, H.TYPE1[E.type])), h('h3', {}, e.h), e.y.length ? h('div', { class: 'muted', style: { fontFamily: 'var(--serif)', fontSize: '16px' } }, e.y.join(' · ')) : null);
  box.append(h('div', { class: 'kv' }, h('div', {}, h('b', {}, nf(e.count)), 'כתבות'), h('div', {}, h('b', {}, fmtDate(e.first)), 'הופעה ראשונה'), h('div', {}, h('b', {}, fmtDate(e.last)), 'הופעה אחרונה'), H.paperKeys.filter(p => e.papers[p]).map(p => h('div', {}, h('b', { style: { color: H.pcol(p) } }, nf(e.papers[p])), H.pname(p)))));
  box.append(h('div', { class: 'chips', style: { marginBottom: '10px' } },
    h('button', { class: 'btn sm pri', onclick: () => H.addEnt(E.type, e.key) }, 'פתח בחיפוש'),
    h('button', { class: 'btn sm', onclick: () => { UI.tl.subj = { kind: 'ent', type: E.type, key: e.key }; UI.tl.sel = null; H.showTab('timeline'); } }, 'השוואה בין עיתונים'),
    h('button', { class: 'btn sm', onclick: () => H.openList({ title: e.h, arts: e.arts, filter: { ents: [{ type: E.type, key: e.key }] } }) }, `כל ${nf(e.count)} הכתבות`)));
  const ch = h('div'); box.append(ch);
  const buckets = allBuckets('quarter'), idx = new Map(buckets.map((k, i) => [k, i])), cell = buckets.map(() => ({}));
  for (const a of e.arts) { const i = idx.get(bucketKey(a.d, 'quarter')); (cell[i][a.p] = cell[i][a.p] || []).push(a); }
  const series = H.paperKeys.map(p => ({ key: p, label: H.pname(p), color: H.pcol(p) }));
  setTimeout(() => H.timeBars(ch, { buckets, series, gran: 'quarter', height: 110, aria: 'התפלגות בזמן', cell: (bi, si) => cell[bi][series[si].key] || [], onClick: (arts, k) => H.openList({ title: `${e.h} · ${bucketLabel(k)}`, arts }) }), 0);
  for (const t of Object.keys(H.TYPES)) {
    const c = new Map(); for (const a of e.arts) for (const k of a['k_' + t]) { if (t === E.type && k === e.key) continue; c.set(k, (c.get(k) || 0) + 1); }
    const top = [...c.entries()].sort((a, b) => b[1] - a[1]).slice(0, 10); if (!top.length) continue;
    box.append(h('div', { class: 'etype' }, h('b', {}, 'מופיעים לצידה: ' + H.TYPES[t]), h('div', { class: 'chips' }, top.map(([k, n]) => {
      const o = H.entity(t, k);
      return h('button', { class: 'chip t-' + t, title: 'הכתבות שבהן שתיהן מופיעות', onclick: () => H.openList({ title: `${e.h} + ${o.h}`, arts: e.arts.filter(a => a['k_' + t].includes(k)), filter: { ents: [{ type: E.type, key: e.key }, { type: t, key: k }] } }) }, o.h, h('span', { class: 'muted' }, nf(n)));
    }))));
  }
}

/* ---------- על הנתונים ---------- */
function buildAbout() {
  const v = $('#view-about'); v.innerHTML = '';
  const cnt = p => H.A.filter(a => a.p === p).length;
  const rng = p => { const l = H.A.filter(a => a.p === p); return l[0].d.slice(0, 4) + '–' + l[l.length - 1].d.slice(0, 4); };
  const terms = p => [...new Set(H.A.filter(a => a.p === p).map(a => a.t.join('; ')))].join(' | ');
  v.append(h('div', { class: 'prose', html: `
    <h2>על הנתונים ועל השיטה</h2>
    <p>האתר מציג ניתוח של כתבות מן העיתונות היידית ההיסטורית, שנאספו מן האתר של הספרייה הלאומית לפי מונחי חיפוש, ונותחו (סיכום, ישויות, נושאים, סוגה, מרכזיות המונח ורלוונטיות למחקר) על בסיס טקסט ה־OCR המתוקן. כל רשומה מקושרת לכתבה המקורית ולתמונות העמוד.</p>
    <h3>מה בדגימה</h3>
    <table><tr><th>עיתון</th><th>כתבות</th><th>שנים</th><th>מונחי איסוף</th></tr>
    ${H.paperKeys.map(p => `<tr><td>${esc(H.pname(p))}</td><td>${nf(cnt(p))}</td><td>${ltr(rng(p))}</td><td>${esc(terms(p))}</td></tr>`).join('')}</table>
    <div class="note"><b>חשוב לפרשנות:</b> מונחי האיסוף שונים בין העיתונים, ולכן ההבדלים בנפח בין עיתונים משקפים בעיקר את דגימת האיסוף ולא את חשיבות הנושא בעיתון. עדיף להשוות <i>מגמות</i> ו<i>הרכב</i> (אחוזים בתוך עיתון), ולהשוות בין עיתונים בנושאים שנאספו בכולם (למשל מרוקו בדער פריינד ובהיינט).</div>
    <h3>מה מחושב אוטומטית ומה בא מהגיליון</h3>
    <ul>
      <li><b>מן הגיליון, כפי שהוא:</b> עיתון, תאריך, קישור, סיכום, "מה נאמר על המונח", מרכזיות, אנשים, מקומות, ארגונים, קבוצות אוכלוסייה, נושאים, סוגה, רלוונטיות, והטקסט ביידיש.</li>
      <li><b>איחוד שמות ישויות:</b> שמות זהים בעברית (בלי "ה" הידיעה ובלי גרשיים) נספרים כישות אחת, והכתיב היידי השכיח מוצג לצידם. אין כאן איחוד סמנטי: "הסולטאן" ו"סולטאן מרוקו" נשארים נפרדים.</li>
      <li><b>נושאי-על:</b> קיבוץ אוטומטי של שדה "נושאים" לפי מילות מפתח (13 קבוצות). לכל כתבה יש תיוג מרובה (לסינון) ונושא ראשי אחד (לגרפים מחולקים). זהו כלי גלישה, והוא עשוי לטעות; אפשר לבדוק כל תוצאה במגירה.</li>
      <li><b>"הקשר יהודי":</b> כתבה שבה קבוצות האוכלוסייה כוללות יהודים, או שנושאיה עוסקים ביהודים, בציונות, בקהילות או בעלילות דם. היוריסטיקה גסה, לצורך מגמות בלבד.</li>
      <li><b>אירועי רקע בגרפים:</b> ידע היסטורי כללי, לא נגזר מן הגיליון, ומיועד לעזור בקריאת פסגות בגרפים.</li>
    </ul>
    <h3>חיפוש ביידיש</h3>
    <p>הנרמול מתעלם מניקוד ומסימני פּאַסאך/קאמץ, מאחד לִיגטורות (װ=וו, ײ=יי, ױ=וי) ואותיות סופיות. חיפוש בטקסט ביידיש עובד על ה־OCR המתוקן, וה־OCR עלול להכיל שיבושים; מילה שלא נמצאה אינה בהכרח לא קיימת.</p>
    <h3>תמונות</h3>
    <p>התמונות נטענות מתיקיית הכונן של המעבדה לפי מזהה הכתבה (שם התיקייה והקבצים). אם הקובץ אינו נגיש, או שאין תיקיה, מוצג הקישור לעמוד בספרייה הלאומית.</p>
    <h3>הורדות</h3>
    <p><button class="btn" id="dlAll">כל הכתבות כ־CSV</button> <a class="btn" href="data.json" download>data.json</a></p>
    <h3>עדכון הנתונים</h3>
    <p>כשהגיליון גדל: מורידים אותו כ־xlsx או csv, מריצים <code>python build_data.py analysis.xlsx imgmap.json</code>, ומעלים את <code>data.json</code> ו־<code>ocr.json</code> החדשים לריפוזיטורי. פרטים ב־README.</p>
    <p class="muted small">נבנה במעבדת אליהו, אוניברסיטת חיפה. נתונים נכון ל־${esc(H.meta.built)} · ${nf(H.A.length)} רשומות.</p>` }));
  $('#dlAll').onclick = () => H.artsCSV(H.A, 'all-articles');
}

/* ---------- ניווט ---------- */
const TABS = { search: 'חיפוש', timeline: 'ציר זמן והשוואה', entities: 'ישויות', overview: 'תמונה היסטורית רחבה', about: 'על הנתונים' };
const built = {};
H.showTab = function (t) {
  if (!TABS[t]) t = 'search';
  UI.tab = t;
  $$('.view').forEach(v => v.classList.toggle('on', v.id === 'view-' + t));
  $$('.tab').forEach(b => b.setAttribute('aria-selected', b.dataset.t === t));
  if (!$('#modal').classList.contains('on')) history.replaceState(null, '', '#' + t);
  if (!built[t]) { built[t] = 1; ({ timeline: buildTimeline, entities: buildEntities, overview: () => H.buildOverview(), about: buildAbout }[t] || (() => { }))(); }
  else if (t === 'timeline') drawTL(); else if (t === 'overview') H.relayoutOverview && H.relayoutOverview();
  scrollTo(0, 0);
};
function route() {
  const hs = location.hash.replace(/^#/, '');
  if (hs.startsWith('a/')) { const a = H.byId.get(decodeURIComponent(hs.slice(2))); if (a) { if (!built.search) { } H.openArticle(a, null); return; } }
  if (TABS[hs]) H.showTab(hs);
}
H.boot = async function () {
  const nav = $('#tabs');
  for (const [k, l] of Object.entries(TABS)) nav.append(h('button', { class: 'tab', role: 'tab', 'data-t': k, 'aria-selected': k === 'search', onclick: () => H.showTab(k) }, l));
  try { await H.load(); }
  catch (e) {
    $('#view-search').innerHTML = `<div class="panel"><h3>לא ניתן לטעון את data.json</h3><p class="muted">אם פתחתם את index.html ישירות מהמחשב (file://), הדפדפן חוסם טעינת קבצים. הפעילו שרת מקומי (<code>python -m http.server</code>) או העלו ל-GitHub Pages. אפשר גם לבחור כאן קובץ data.json:</p><input type="file" id="pick" accept=".json"></div>`;
    $('#pick').onchange = async ev => { H.init(JSON.parse(await ev.target.files[0].text())); start(); };
    return;
  }
  start();
};
function start() {
  UI.F = H.newF();
  buildSearch(); renderStats(); renderSearch(); built.search = 1;
  $('#modal').addEventListener('click', e => { if (e.target.id === 'modal') H.closeArticle(); });
  $('#scrim').addEventListener('click', () => { if ($('#modal').classList.contains('on')) H.closeArticle(); H.closeDrawer(); });
  $('#drawer .x').onclick = H.closeDrawer;
  $('#lightbox').addEventListener('click', e => { if (e.target.id === 'lightbox') e.currentTarget.classList.remove('on'); });
  addEventListener('keydown', e => {
    if (e.key === 'Escape') { if ($('#lightbox').classList.contains('on')) $('#lightbox').classList.remove('on'); else if ($('#modal').classList.contains('on')) H.closeArticle(); else H.closeDrawer(); }
    else if ($('#modal').classList.contains('on') && !/INPUT|TEXTAREA|SELECT/.test(document.activeElement.tagName)) { if (e.key === 'ArrowLeft') stepArticle(1); if (e.key === 'ArrowRight') stepArticle(-1); }
  });
  addEventListener('hashchange', route);
  let rz; addEventListener('resize', () => { clearTimeout(rz); rz = setTimeout(() => { if (UI.tab === 'timeline') drawTL(); else if (UI.tab === 'overview') H.relayoutOverview && H.relayoutOverview(); else if (UI.tab === 'search') renderMini(); else if (UI.tab === 'entities' && UI.ent.sel) drawEntDetail(); $('#togSide').style.display = innerWidth < 1100 ? '' : 'none'; }, 200); });
  $('#togSide').style.display = innerWidth < 1100 ? '' : 'none';
  route();
}
document.addEventListener('DOMContentLoaded', H.boot);
