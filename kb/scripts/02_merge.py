#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Step 2: merge the resolution outputs into the managed knowledge base.

Inputs (kb/work/):  ent_<type>_<n>.json   entity clusters per batch (+ contextual resolutions, drops)
                    vocab.json            controlled topic concepts + events
                    topicmap_<n>.json     free-text topic string -> concept/event ids
Outputs (kb/):      entities.json         every entity: id, type, labels, description, hierarchy fields, qid
                    surface_forms.json    {src_type: {surface key: [entity ids]}}  +  contextual  +  dropped
                    redirects.json        merged-away id -> canonical id (e.g. two ids with the same Wikidata QID)
"""
import sys, os, glob, json, collections, re
sys.path.insert(0, os.path.dirname(__file__))
from kblib import *
if hasattr(sys.stdout, 'reconfigure'): sys.stdout.reconfigure(encoding='utf-8')

PREFIX_TYPE = {'ppl': 'ppl', 'pl': 'pl', 'org': 'org', 'grp': 'grp', 'ev': 'ev', 'top': 'top'}
LIST_F = ('en_alt', 'related', 'participants')
log = []

E = {}                                  # id -> entity
SF = {t: collections.defaultdict(list) for t in TYPES}   # src type -> key -> [ids]
CTX = {t: {} for t in TYPES}            # src type -> key -> {article: id|None}
DROP = {t: {} for t in TYPES}


def add_entity(rec, src):
    eid = rec['id']
    t = PREFIX_TYPE[eid.split(':')[0]]
    cur = E.get(eid)
    if not cur:
        cur = E[eid] = {'id': eid, 'type': t, 'src': []}
    for k, v in rec.items():
        if k in ('id', 'keys', 'qid_auto') or v in (None, '', []): continue
        if k in LIST_F:
            cur[k] = list(dict.fromkeys((cur.get(k) or []) + list(v)))
        elif k not in cur or cur[k] in (None, ''):
            cur[k] = v
        elif cur[k] != v and k in ('parent', 'country', 'broader', 'qid'):
            log.append(f'conflict {eid}.{k}: {cur[k]} (kept) vs {v} ({src})')
    if 'qid' not in rec and rec.get('qid_auto') and not cur.get('qid'):
        cur.setdefault('qid_auto', rec['qid_auto'])
    cur['src'].append(src)
    return cur


# ---- entity batches
for p in sorted(glob.glob(os.path.join(WORK, 'ent_*_*.json'))):
    if p.endswith('.cand.json'): continue
    src_t = re.match(r'ent_(\w+?)_\d+\.json', os.path.basename(p)).group(1)
    d = load_json(p)
    for rec in d.get('entities', []):
        add_entity(rec, os.path.basename(p))
        for k in rec.get('keys', []):
            if rec['id'] not in SF[src_t][k]: SF[src_t][k].append(rec['id'])
    for c in d.get('contextual', []):
        CTX[src_t][c['key']] = dict(c.get('articles') or {})
    for x in d.get('drop', []):
        k = x['key'] if isinstance(x, dict) else x
        DROP[src_t][k] = x.get('why', '') if isinstance(x, dict) else ''

# ---- vocabulary
V = load_json(os.path.join(WORK, 'vocab.json'), {'concepts': [], 'events': []})
for c in V.get('concepts', []): add_entity(c, 'vocab.json')
for ev in V.get('events', []): add_entity(ev, 'vocab.json')
# vocab-level review decisions (qids for events)
for p in glob.glob(os.path.join(WORK, 'vocab_qids.json')):
    for eid, q in load_json(p).items():
        if eid in E: E[eid]['qid'] = q

# ---- topic string mapping
for p in sorted(glob.glob(os.path.join(WORK, 'topicmap_*.json'))):
    for k, ids in load_json(p).get('map', {}).items():
        SF['top'][k] = list(dict.fromkeys(SF['top'].get(k, []) + ids))

# ---- dangling references -> report (and stub so nothing breaks)
refs = collections.Counter()
def ref_ids(e):
    for f in ('parent', 'country', 'broader', 'place'):
        if e.get(f): yield e[f]
    for f in ('related', 'participants'):
        yield from e.get(f) or []
for e in list(E.values()):
    for r in ref_ids(e):
        if r not in E: refs[r] += 1
for t in TYPES:
    for k, ids in SF[t].items():
        for r in ids:
            if r not in E: refs[r] += 1
    for k, m in CTX[t].items():
        for r in m.values():
            if r and r not in E: refs[r] += 1
stubs = load_json(os.path.join(WORK, 'stubs.json'), {})
for r in refs:
    if r in stubs:
        add_entity(dict(stubs[r], id=r), 'stubs.json')
MR = load_json(os.path.join(WORK, 'manual_redirects.json'), {}) or {}
missing = {r: n for r, n in refs.items() if r not in E and r not in MR}

# ---- QID-based merging (same Wikidata item under two ids)
def qid_of(e): return e.get('qid') or None
by_q = collections.defaultdict(list)   # merge only within the same type (a group and an army may share an item)
for e in E.values():
    if qid_of(e): by_q[(e['type'] if e['type'] not in ('top', 'ev') else 'tev', qid_of(e))].append(e['id'])
mention_n = collections.Counter()
for t in TYPES:
    for k, ids in SF[t].items():
        for i in ids: mention_n[i] += 1
    for m in CTX[t].values():
        for i in m.values():
            if i: mention_n[i] += 1
R = {}
def absorb(i, canon):
    R[i] = canon
    if i not in E: return
    if canon not in E:
        E[canon] = dict(E[i], id=canon); del E[i]; return
    for k, v in E[i].items():
        if k in ('id', 'src'): continue
        if k in LIST_F: E[canon][k] = list(dict.fromkeys((E[canon].get(k) or []) + v))
        elif k not in E[canon] or E[canon][k] in (None, ''): E[canon][k] = v
    E[canon]['src'] += E[i]['src']
    del E[i]
# manual redirects (kb/work/manual_redirects.json): merge duplicates the QID step cannot catch
for i, canon in (load_json(os.path.join(WORK, 'manual_redirects.json'), {}) or {}).items():
    absorb(i, canon)
for q, ids in by_q.items():
    ids = [i for i in ids if i in E]
    if len(ids) < 2: continue
    # prefer vocabulary ids, then the one with most surface forms
    canon = sorted(ids, key=lambda i: ('vocab.json' not in E[i]['src'], -mention_n[i], i))[0]
    for i in ids:
        if i != canon: absorb(i, canon)
def rd(i):
    seen = set()
    while i in R and i not in seen: seen.add(i); i = R[i]
    return i
for e in E.values():
    for f in ('parent', 'country', 'broader', 'place'):
        if e.get(f): e[f] = rd(e[f])
    for f in ('related', 'participants'):
        if e.get(f): e[f] = list(dict.fromkeys(rd(x) for x in e[f]))
    if e.get('parent') == e['id']: del e['parent']
    if e.get('broader') == e['id']: del e['broader']
for t in TYPES:
    for k in SF[t]: SF[t][k] = list(dict.fromkeys(rd(x) for x in SF[t][k]))
    for k in CTX[t]: CTX[t][k] = {a: (rd(x) if x else None) for a, x in CTX[t][k].items()}

# ---- hierarchy cycle guard
for f in ('parent', 'broader'):
    for e in E.values():
        seen, cur = {e['id']}, e.get(f)
        while cur and cur in E:
            if cur in seen:
                log.append(f'cycle via {f} at {e["id"]} -> removed'); e.pop(f, None); break
            seen.add(cur); cur = E[cur].get(f)

# ---- surface labels per entity (aliases)
for t in TYPES:
    for k, ids in SF[t].items():
        for i in ids:
            if i in E: E[i].setdefault('aliases', []).append(k)
for e in E.values():
    if 'aliases' in e: e['aliases'] = sorted(set(e['aliases']) - {e.get('he')})
    e['src'] = sorted(set(e['src']))

save_json(os.path.join(KB, 'entities.json'), dict(sorted(E.items())))
save_json(os.path.join(KB, 'surface_forms.json'), {'map': {t: dict(sorted(SF[t].items())) for t in TYPES},
                                                   'contextual': CTX, 'dropped': DROP})
save_json(os.path.join(KB, 'redirects.json'), R)
cnt = collections.Counter(e['type'] for e in E.values())
print('entities by type:', dict(cnt))
print('with qid:', sum(1 for e in E.values() if e.get('qid')), ' merged by qid:', len(R))
print('surface keys:', {t: len(SF[t]) for t in TYPES}, ' contextual:', {t: len(CTX[t]) for t in TYPES}, ' dropped:', {t: len(DROP[t]) for t in TYPES})
if missing:
    print(f'{len(missing)} dangling referenced ids (add to kb/work/stubs.json):')
    for r, n in sorted(missing.items(), key=lambda x: -x[1])[:60]: print('  ', r, n)
save_json(os.path.join(WORK, 'dangling.json'), missing)
for l in log[:40]: print('log:', l)
print(f'{len(log)} log lines')
