'use strict';
/* ====== גרפים (SVG ו-HTML), ללא תלות חיצונית ====== */

function chartBase(host, o) {
  host.innerHTML = '';
  const W = Math.max(320, host.clientWidth || 800), Ht = o.height || 190;
  const m = { l: 44, r: 8, t: o.events ? 78 : 10, b: 24 };
  const svg = S('svg', { viewBox: `0 0 ${W} ${Ht + m.t + m.b}`, width: '100%', role: 'img', 'aria-label': o.aria || 'גרף' });
  svg.style.height = (Ht + m.t + m.b) + 'px'; svg.style.direction = 'ltr';
  const nb = o.buckets.length, bw = (W - m.l - m.r) / nb;
  const X = bi => m.l + (bi + .5) * bw;
  const ymax = o.ymax || 1;
  const Y = v => m.t + Ht - (v / ymax) * Ht;
  // רשת
  const g = S('g', { class: 'axis' });
  const ticks = o.yMode === 'pct' ? [0, .25, .5, .75, 1] : niceTicks(ymax);
  for (const tv of ticks) {
    g.append(S('line', { x1: m.l, x2: W - m.r, y1: Y(tv), y2: Y(tv), stroke: '#e6ecf0' }));
    g.append(S('text', { x: m.l - 5, y: Y(tv) + 4, 'text-anchor': 'end' }, o.yMode === 'pct' ? Math.round(tv * 100) + '%' : nf(tv)));
  }
  // תוויות X
  o.buckets.forEach((k, i) => {
    let lab = null;
    if (/^\d{4}$/.test(k)) lab = k; else if (/Q1$/.test(k)) lab = k.slice(0, 4); else if (/-01$/.test(k)) lab = k.slice(0, 4);
    if (lab) {
      g.append(S('text', { x: X(i) - (/^\d{4}$/.test(k) ? 0 : bw / 2), y: m.t + Ht + 16, 'text-anchor': /^\d{4}$/.test(k) ? 'middle' : 'start' }, lab));
      if (!/^\d{4}$/.test(k)) g.append(S('line', { x1: X(i) - bw / 2, x2: X(i) - bw / 2, y1: m.t + Ht, y2: m.t + Ht + 5, stroke: '#9fb0ba' }));
    }
  });
  svg.append(g);
  if (o.range) { // מחוץ לטווח הדגימה של העיתון
    const [d0, d1] = o.range;
    o.buckets.forEach((k, i) => { const [f, t] = bucketRange(k); if (t < d0 || f > d1) svg.append(S('rect', { x: X(i) - bw / 2, y: m.t, width: bw, height: Ht, fill: '#e9edf0' })); });
  }
  if (o.sel) { const si = o.buckets.indexOf(o.sel); if (si >= 0) svg.append(S('rect', { x: X(si) - bw / 2, y: m.t, width: bw, height: Ht, fill: '#00a9d4', 'fill-opacity': .18 })); }
  // אירועי רקע
  if (o.events) {
    const gE = S('g');
    for (const [d, lab] of H.EVENTS) {
      const bk = bucketKey(d, o.gran); const bi = o.buckets.indexOf(bk);
      if (bi < 0) continue;
      let frac = .5;
      if (o.gran === 'month') frac = (+d.slice(8, 10) - 1) / 30; else if (o.gran === 'quarter') frac = ((+d.slice(5, 7) - 1) % 3) / 3 + (+d.slice(8, 10) - 1) / 90; else frac = (+d.slice(5, 7) - 1) / 12;
      const x = m.l + (bi + frac) * bw;
      gE.append(S('line', { x1: x, x2: x, y1: m.t - 6, y2: m.t + Ht, stroke: '#c9822b', 'stroke-dasharray': '3 3', 'stroke-width': 1 }));
      const tx = S('text', { x, y: m.t - 10, transform: `rotate(-50 ${x} ${m.t - 10})`, 'text-anchor': 'start', style: 'font-size:11px;fill:#8a5a14' }, lab);
      gE.append(tx);
    }
    svg.append(gE);
  }
  host.append(svg);
  return { svg, W, Ht, m, bw, X, Y, nb };
}
function niceTicks(max) {
  if (max <= 4) return Array.from({ length: Math.ceil(max) + 1 }, (_, i) => i);
  const step = [1, 2, 5, 10, 20, 25, 50, 100, 200, 500].find(s => max / s <= 5) || 1000;
  const out = []; for (let v = 0; v <= max + 1e-9; v += step) out.push(v); return out;
}

/* עמודות מוערמות על ציר זמן */
H.timeBars = function (host, o) {
  const nb = o.buckets.length, ns = o.series.length;
  const cells = o.buckets.map((_, bi) => o.series.map((_, si) => o.cell(bi, si)));
  const totals = cells.map(r => r.reduce((s, a) => s + a.length, 0));
  o.ymax = o.yMode === 'pct' ? 1 : (o.ymax || Math.max(1, ...totals));
  const B = chartBase(host, o);
  const gB = S('g');
  cells.forEach((row, bi) => {
    let acc = 0;
    row.forEach((arts, si) => {
      if (!arts.length) return;
      const v = o.yMode === 'pct' ? arts.length / (totals[bi] || 1) : arts.length;
      const y0 = B.Y(acc + v), y1 = B.Y(acc); acc += v;
      const s = o.series[si];
      const r = S('rect', { x: B.X(bi) - B.bw / 2 + Math.min(1, B.bw * .06), y: y0, width: Math.max(1, B.bw - Math.min(2, B.bw * .12)), height: Math.max(.5, y1 - y0), fill: s.color, style: 'cursor:pointer' });
      r.addEventListener('click', () => o.onClick && o.onClick(arts, o.buckets[bi], s));
      H.tip(r, () => `<b>${esc(bucketLabel(o.buckets[bi]))}</b><br>${esc(s.label)}: ${nf(arts.length)}${o.yMode === 'pct' ? ' (' + pct(arts.length, totals[bi]) + '%)' : ''}`);
      gB.append(r);
    });
  });
  B.svg.append(gB);
  return B;
};

/* קווים */
H.lineChart = function (host, o) {
  const max = Math.max(1, ...o.series.flatMap(s => s.vals.filter(v => v != null)));
  o.ymax = o.ymax || max;
  const B = chartBase(host, o);
  for (const s of o.series) {
    // קטעים רצופים (ערכי null שוברים את הקו)
    let seg = [];
    const flush = () => { if (seg.length > 1) B.svg.append(S('polyline', { points: seg.map(p => p.join(',')).join(' '), fill: 'none', stroke: s.color, 'stroke-width': 2, 'stroke-linejoin': 'round' })); seg = []; };
    s.vals.forEach((v, i) => { if (v == null) flush(); else seg.push([B.X(i), B.Y(v)]); });
    flush();
    s.vals.forEach((v, i) => {
      if (v == null || (!v && !o.showZero)) return;
      const c = S('circle', { cx: B.X(i), cy: B.Y(v), r: v ? 3.6 : 2, fill: s.color, stroke: '#fff', 'stroke-width': 1, style: 'cursor:pointer' });
      c.addEventListener('click', () => o.onClick && o.onClick(s, i));
      H.tip(c, () => `<b>${esc(bucketLabel(o.buckets[i]))}</b><br>${esc(s.label)}: ${o.fmt ? o.fmt(v, s, i) : nf(v)}`);
      B.svg.append(c);
    });
  }
  return B;
};

/* ציר נקודות לפי תאריך: שורה לכל ישות */
H.dotTimeline = function (host, rows, o = {}) {
  host.innerHTML = '';
  const W = Math.max(480, host.clientWidth || 800), rh = 26, m = { l: 8, r: 150, t: 8, b: 24 };
  const d0 = dayNum(H.minD), d1 = dayNum(H.maxD), Hh = rows.length * rh + m.t + m.b;
  const svg = S('svg', { viewBox: `0 0 ${W} ${Hh}`, width: '100%', role: 'img', 'aria-label': 'ציר זמן' }); svg.style.height = Hh + 'px'; svg.style.direction = 'ltr';
  const X = d => m.l + (d - d0) / (d1 - d0) * (W - m.l - m.r);
  const g = S('g', { class: 'axis' });
  for (const y of H.years) { const x = X(dayNum(y + '-01-01')); g.append(S('line', { x1: x, x2: x, y1: m.t, y2: Hh - m.b, stroke: '#eef2f5' })); g.append(S('text', { x: x + 2, y: Hh - 8 }, y)); }
  svg.append(g);
  rows.forEach((r, i) => {
    const cy = m.t + i * rh + rh / 2;
    svg.append(S('line', { x1: m.l, x2: W - m.r, y1: cy, y2: cy, stroke: '#f0f3f5' }));
    const bucket = {};
    for (const a of r.arts) { const k = a.d.slice(0, 7) + a.p; (bucket[k] = bucket[k] || []).push(a); }
    for (const arts of Object.values(bucket)) {
      const a = arts[0], x = X(a._ts);
      const c = S('circle', { cx: x, cy: cy + (['dfr', 'hyt', 'unzerleben'].indexOf(a.p) - 1) * 4, r: 3 + Math.min(4, arts.length - 1), fill: H.pcol(a.p), 'fill-opacity': .85, stroke: '#fff', 'stroke-width': .8, style: 'cursor:pointer' });
      c.addEventListener('click', () => o.onDot && o.onDot(arts, r));
      H.tip(c, () => `<b>${esc(r.label)}</b><br>${esc(H.pname(a.p))} · ${esc(fmtMonth(a.d.slice(0, 7)))}<br>${arts.length} כתבות`);
      svg.append(c);
    }
    const t = S('text', { x: W - m.r + 8, y: cy + 4, style: 'font-size:13px;cursor:pointer;fill:#1d2d38' }, r.label.length > 22 ? r.label.slice(0, 21) + '…' : r.label);
    t.addEventListener('click', () => o.onRow && o.onRow(r));
    svg.append(t);
    svg.append(S('text', { x: W - 4, y: cy + 4, 'text-anchor': 'end', style: 'font-size:11px;fill:#667985' }, nf(r.arts.length)));
  });
  host.append(svg);
};

/* פסי עמודות אופקיים (HTML), אפשר מוערמים לפי עיתון */
H.hbars = function (host, rows, o = {}) {
  host.innerHTML = '';
  const max = Math.max(1, ...rows.map(r => r.total));
  for (const r of rows) {
    const tr = h('div', { class: 'tr' });
    for (const s of r.segs) {
      if (!s.value) continue;
      const seg = h('i', { style: { width: (s.value / max * 100) + '%', background: s.color }, onclick: () => o.onSeg && o.onSeg(r, s) });
      H.tip(seg, () => `<b>${esc(r.label)}</b><br>${esc(s.label)}: ${nf(s.value)}${r.denom ? ' (' + pct(s.value, r.denom) + '%)' : ''}`);
      tr.append(seg);
    }
    host.append(h('div', { class: 'hrow' },
      h('div', { class: 'lb', title: r.label }, h('button', { onclick: () => o.onLabel && o.onLabel(r) }, r.label)),
      tr, h('div', { class: 'v' }, o.fmt ? o.fmt(r) : nf(r.total))));
  }
};

/* 100% מוערם (HTML) */
H.stack100 = function (host, rows, cats, o = {}) {
  host.innerHTML = '';
  for (const r of rows) {
    const total = r.arts.length || 1;
    const tr = h('div', { class: 'tr', style: { height: '24px' } });
    for (const c of cats) {
      const arts = r.arts.filter(a => c.test(a));
      if (!arts.length) continue;
      const p = arts.length / total * 100;
      const seg = h('i', { style: { width: p + '%', background: c.color, color: '#fff', fontSize: '11px', display: 'flex', alignItems: 'center', justifyContent: 'center', overflow: 'hidden' }, onclick: () => o.onSeg && o.onSeg(r, c, arts) }, p > 9 ? Math.round(p) + '%' : '');
      H.tip(seg, () => `<b>${esc(r.label)}</b><br>${esc(c.label)}: ${nf(arts.length)} מתוך ${nf(r.arts.length)} (${pct(arts.length, r.arts.length)}%)`);
      tr.append(seg);
    }
    host.append(h('div', { class: 'hrow', style: { gridTemplateColumns: 'minmax(90px,140px) minmax(0,1fr) 40px' } }, h('div', { class: 'lb', title: r.label }, r.label), tr, h('div', { class: 'v' }, nf(r.arts.length))));
  }
  host.append(h('div', { class: 'legend' }, cats.map(c => h('span', {}, h('i', { class: 'dot', style: { background: c.color } }), c.label))));
};

/* מפת חום (HTML) */
H.heat = function (host, rowL, colL, cell, o = {}) {
  host.innerHTML = '';
  const vals = rowL.flatMap((_, r) => colL.map((_, c) => cell(r, c).v));
  const max = Math.max(1e-9, ...vals);
  const tb = h('table', { class: 'heat' });
  tb.append(h('thead', {}, h('tr', {}, h('th'), colL.map(c => h('th', {}, c.label)))));
  const body = h('tbody');
  rowL.forEach((rl, r) => {
    const tr = h('tr', {}, h('th', { class: 'rl' }, rl.label));
    colL.forEach((cl, c) => {
      const x = cell(r, c), t = x.v / max;
      const bg = `rgba(24,52,69,${(.06 + t * .88).toFixed(3)})`;
      const td = h('td', { style: { background: bg, color: t > .45 ? '#fff' : '#1d2d38' }, onclick: () => x.arts.length && o.onClick && o.onClick(rl, cl, x.arts) },
        o.pctFmt ? o.pctFmt(x) : Math.round(x.v * 1000) / 10 + '%', h('small', {}, nf(x.arts.length)));
      H.tip(td, () => `<b>${esc(rl.label)}</b> × ${esc(cl.label)}<br>${nf(x.arts.length)} כתבות${x.extra ? '<br>' + x.extra : ''}`);
      tr.append(td);
    });
    body.append(tr);
  });
  tb.append(body); host.append(tb);
};

/* קו מגמה קטן (מחרוזת SVG) */
H.spark = function (vals, w = 90, hh = 22, color = '#25485c') {
  const mx = Math.max(1, ...vals), n = vals.length, bw = w / n;
  return `<svg class="spark" width="${w}" height="${hh}" viewBox="0 0 ${w} ${hh}">` +
    vals.map((v, i) => `<rect x="${(i * bw + .5).toFixed(1)}" y="${(hh - v / mx * (hh - 2)).toFixed(1)}" width="${(bw - 1).toFixed(1)}" height="${(v / mx * (hh - 2)).toFixed(1)}" fill="${color}" opacity="${v ? .85 : .12}"/>`).join('') + '</svg>';
};

/* רשת (פריסת כוחות פשוטה) */
H.network = function (host, nodes, links, o = {}) {
  host.innerHTML = '';
  const W = Math.max(480, host.clientWidth || 800), Hh = o.height || 520;
  const n = nodes.length;
  nodes.forEach((d, i) => { const a = i / n * 2 * Math.PI; d.x = W / 2 + Math.cos(a) * W * .3; d.y = Hh / 2 + Math.sin(a) * Hh * .3; d.vx = 0; d.vy = 0; d.r = 5 + Math.sqrt(d.count) * 1.5; });
  const idx = new Map(nodes.map((d, i) => [d.key, i]));
  const L = links.map(l => ({ ...l, a: idx.get(l.a), b: idx.get(l.b) })).filter(l => l.a != null && l.b != null);
  for (let it = 0; it < 320; it++) {
    const cool = 1 - it / 320;
    for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) {
      const A = nodes[i], B = nodes[j]; let dx = A.x - B.x, dy = A.y - B.y; let d2 = dx * dx + dy * dy + .01; const d = Math.sqrt(d2);
      const f = 2600 / d2 * cool; dx /= d; dy /= d; A.vx += dx * f; A.vy += dy * f; B.vx -= dx * f; B.vy -= dy * f;
    }
    for (const l of L) {
      const A = nodes[l.a], B = nodes[l.b]; const dx = B.x - A.x, dy = B.y - A.y; const d = Math.sqrt(dx * dx + dy * dy) + .01;
      const target = 70 + 120 / Math.sqrt(l.w); const f = (d - target) * .012 * Math.min(3, Math.sqrt(l.w) / 2);
      A.vx += dx / d * f; A.vy += dy / d * f; B.vx -= dx / d * f; B.vy -= dy / d * f;
    }
    for (const d of nodes) {
      d.vx += (W / 2 - d.x) * .004; d.vy += (Hh / 2 - d.y) * .006;
      d.x += Math.max(-12, Math.min(12, d.vx)); d.y += Math.max(-12, Math.min(12, d.vy)); d.vx *= .78; d.vy *= .78;
      d.x = Math.max(d.r + 6, Math.min(W - d.r - 6, d.x)); d.y = Math.max(d.r + 12, Math.min(Hh - d.r - 12, d.y));
    }
  }
  const svg = S('svg', { viewBox: `0 0 ${W} ${Hh}`, width: '100%', role: 'img', 'aria-label': 'רשת' }); svg.style.height = Hh + 'px'; svg.style.direction = 'ltr';
  const wmax = Math.max(1, ...L.map(l => l.w));
  for (const l of L) {
    const A = nodes[l.a], B = nodes[l.b];
    const ln = S('line', { x1: A.x, y1: A.y, x2: B.x, y2: B.y, stroke: '#7f98a6', 'stroke-opacity': .25 + .5 * l.w / wmax, 'stroke-width': .8 + 5 * l.w / wmax, style: 'cursor:pointer' });
    ln.addEventListener('click', () => o.onLink && o.onLink(A, B, l));
    H.tip(ln, () => `<b>${esc(A.label)} + ${esc(B.label)}</b><br>${nf(l.w)} כתבות משותפות`);
    svg.append(ln);
  }
  for (const d of nodes) {
    const g = S('g', { style: 'cursor:pointer' });
    g.append(S('circle', { cx: d.x, cy: d.y, r: d.r, fill: d.color || '#25485c', 'fill-opacity': .88, stroke: '#fff', 'stroke-width': 1.5 }));
    g.append(S('text', { x: d.x, y: d.y - d.r - 4, 'text-anchor': 'middle', style: 'font-size:12.5px;fill:#1d2d38;paint-order:stroke;stroke:#fff;stroke-width:3px' }, d.label));
    g.addEventListener('click', () => o.onNode && o.onNode(d));
    H.tip(g, () => `<b>${esc(d.label)}</b><br>${nf(d.count)} כתבות`);
    svg.append(g);
  }
  host.append(svg);
};
