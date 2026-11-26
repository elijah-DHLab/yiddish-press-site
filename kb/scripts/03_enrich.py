#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Step 3: enrich entities from Wikidata and build the relation graph (ontology).

Inputs:   kb/entities.json (from 02_merge.py)
Outputs:  kb/wikidata.json   {qid: labels, descriptions, coordinates, dates, image, wikipedia titles, typed claims}
          kb/relations.json  [[subject, predicate, object, source], ...]   source = "kb" (curated) | "wikidata"
Predicates (see kb/README.md): located_in, part_of, broader, country, related, location, participant, member_of
Run with --offline to rebuild relations from the cached kb/wikidata.json without network access.
"""
import sys, os, json, collections, re
sys.path.insert(0, os.path.dirname(__file__))
from kblib import *
import wd
if hasattr(sys.stdout, 'reconfigure'): sys.stdout.reconfigure(encoding='utf-8')

E = load_json(os.path.join(KB, 'entities.json'))
WDP = os.path.join(KB, 'wikidata.json')
W = load_json(WDP, {})
qids = sorted({e['qid'] for e in E.values() if e.get('qid')})
offline = '--offline' in sys.argv
REL_P = ['P31', 'P17', 'P131', 'P27', 'P102', 'P710', 'P276', 'P361', 'P463', 'P106', 'P39', 'P36', 'P150']

if not offline:
    need = [q for q in qids if q not in W or '--refresh' in sys.argv]
    print('fetching', len(need), 'items')
    for k in range(0, len(need), 80):
        chunk = need[k:k + 80]
        vals = ' '.join('wd:' + q for q in chunk)
        rows = wd.sparql("""SELECT ?item ?en ?he ?yi ?den ?dhe ?coord ?img ?hew ?enw ?yiw ?b ?d ?s ?e WHERE {
          VALUES ?item { %s }
          OPTIONAL { ?item rdfs:label ?en FILTER(LANG(?en)="en") } OPTIONAL { ?item rdfs:label ?he FILTER(LANG(?he)="he") }
          OPTIONAL { ?item rdfs:label ?yi FILTER(LANG(?yi)="yi") }
          OPTIONAL { ?item schema:description ?den FILTER(LANG(?den)="en") } OPTIONAL { ?item schema:description ?dhe FILTER(LANG(?dhe)="he") }
          OPTIONAL { ?item wdt:P625 ?coord } OPTIONAL { ?item wdt:P18 ?img }
          OPTIONAL { ?hew schema:about ?item; schema:isPartOf <https://he.wikipedia.org/> }
          OPTIONAL { ?enw schema:about ?item; schema:isPartOf <https://en.wikipedia.org/> }
          OPTIONAL { ?yiw schema:about ?item; schema:isPartOf <https://yi.wikipedia.org/> }
          OPTIONAL { ?item wdt:P569 ?b } OPTIONAL { ?item wdt:P570 ?d }
          OPTIONAL { ?item wdt:P580|wdt:P571|wdt:P585 ?s } OPTIONAL { ?item wdt:P582|wdt:P576 ?e }
        }""" % vals)
        got = {}
        for r in rows:
            q = r['item']['value'].rsplit('/', 1)[1]
            g = lambda x: r.get(x, {}).get('value', '')
            o = got.setdefault(q, {})
            for f in ('en', 'he', 'yi', 'den', 'dhe', 'img', 'hew', 'enw', 'yiw'):
                if g(f) and f not in o: o[f] = g(f)
            if g('coord') and 'coord' not in o:
                m = re.match(r'Point\(([-\d.]+) ([-\d.]+)\)', g('coord'))
                if m: o['lon'], o['lat'] = round(float(m.group(1)), 4), round(float(m.group(2)), 4)
            for f, nm in (('b', 'born'), ('d', 'died'), ('s', 'start'), ('e', 'end')):
                if g(f) and nm not in o: o[nm] = g(f)[:10].lstrip('+')
        rows = wd.sparql("""SELECT ?item ?p ?o WHERE { VALUES ?item { %s } VALUES ?p { %s }
                            ?item ?p ?o . FILTER(ISIRI(?o)) }""" % (vals, ' '.join('wdt:' + p for p in REL_P)))
        for r in rows:
            q = r['item']['value'].rsplit('/', 1)[1]
            p = r['p']['value'].rsplit('/', 1)[1]
            o = r['o']['value'].rsplit('/', 1)[1]
            if re.match(r'Q\d+$', o): got.setdefault(q, {}).setdefault('claims', {}).setdefault(p, []).append(o)
        for q in chunk:
            o = got.get(q, {})
            for f in ('hew', 'enw', 'yiw'):
                if f in o: o[f] = o[f].rsplit('/', 1)[1]
            if 'img' in o: o['img'] = o['img'].rsplit('/', 1)[1]
            W[q] = o
        print(f'  {min(k + 80, len(need))}/{len(need)}', flush=True)
    # labels for occupation / position / instance-of values (for display)
    lab_need = sorted({v for o in W.values() for p in ('P106', 'P39', 'P31') for v in (o.get('claims') or {}).get(p, [])} - set(W.get('_labels', {})))
    L = W.setdefault('_labels', {})
    for k in range(0, len(lab_need), 200):
        chunk = lab_need[k:k + 200]
        rows = wd.sparql("""SELECT ?item ?en ?he WHERE { VALUES ?item { %s }
          OPTIONAL { ?item rdfs:label ?en FILTER(LANG(?en)="en") } OPTIONAL { ?item rdfs:label ?he FILTER(LANG(?he)="he") } }""" % ' '.join('wd:' + q for q in chunk))
        for r in rows:
            q = r['item']['value'].rsplit('/', 1)[1]
            L[q] = [r.get('he', {}).get('value', ''), r.get('en', {}).get('value', '')]
    save_json(WDP, W)

# ---------- relations ----------
by_q = {}
for e in E.values():
    if e.get('qid'): by_q.setdefault(e['qid'], e['id'])
rels, seen = [], set()
def add(s, p, o, src):
    if not o or s == o or o not in E: return
    if (s, p, o) in seen: return
    seen.add((s, p, o)); rels.append([s, p, o, src])

for e in E.values():
    i, t = e['id'], e['type']
    if e.get('parent'):
        add(i, {'pl': 'located_in', 'grp': 'broader', 'org': 'part_of'}.get(t, 'part_of'), e['parent'], 'kb')
    if e.get('broader'): add(i, 'broader', e['broader'], 'kb')
    if e.get('country'): add(i, 'country', e['country'], 'kb')
    if e.get('place'): add(i, 'location', e['place'], 'kb')
    for x in e.get('participants') or []: add(i, 'participant', x, 'kb')
    for x in e.get('related') or []: add(i, 'related', x, 'kb')
# from Wikidata, only between entities that exist in our KB
WMAP = {'P131': 'located_in', 'P17': 'country', 'P27': 'country', 'P102': 'member_of', 'P463': 'member_of',
        'P710': 'participant', 'P276': 'location', 'P361': 'part_of', 'P150': None, 'P36': None}
for e in E.values():
    o = W.get(e.get('qid') or '', {})
    for p, vals in (o.get('claims') or {}).items():
        pred = WMAP.get(p)
        if not pred: continue
        if e['type'] == 'pl' and p == 'P17' and e.get('parent'): continue   # curated parent wins for places
        if e['type'] == 'pl' and p == 'P131' and e.get('parent'): continue
        for v in vals:
            if v in by_q: add(e['id'], pred, by_q[v], 'wikidata')
    # inverse: capital / contains
    for v in (o.get('claims') or {}).get('P36', []):
        if v in by_q and not E[by_q[v]].get('parent'): add(by_q[v], 'located_in', e['id'], 'wikidata')

save_json(os.path.join(KB, 'relations.json'), rels, compact=False)
c = collections.Counter((r[1], r[3]) for r in rels)
print('relations:', len(rels), dict(c))
print('entities with wikidata:', sum(1 for e in E.values() if e.get('qid')), '/', len(E),
      ' with coords:', sum(1 for e in E.values() if 'lat' in W.get(e.get('qid') or '', {})))
