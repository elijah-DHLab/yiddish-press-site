#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Wikidata helpers (search API + batched SPARQL for details, with polite rate limiting).

CLI:
  python kb/scripts/wd.py search "Fez" "Mulai Hafid" ...      quick look-up (top candidates)
  python kb/scripts/wd.py get Q80985 Q123 ...                    show items
  python kb/scripts/wd.py candidates kb/work/ent_pl_1.json [...] fill <file>.cand.json + qid_auto for every entity
       [--only-missing]  skip entities that already have a "qid" key
"""
import sys, os, json, time, re, threading
import requests
from concurrent.futures import ThreadPoolExecutor

API = 'https://www.wikidata.org/w/api.php'
SPARQL = 'https://query.wikidata.org/sparql'
S = requests.Session()
S.headers['User-Agent'] = 'YiddishPressKB/0.3 (digital humanities research project; python-requests)'
_lock = threading.Lock()
_last = [0.0]
MIN_GAP = 0.25  # seconds between API requests (global)


def _throttle():
    with _lock:
        wait = _last[0] + MIN_GAP - time.time()
        if wait > 0: time.sleep(wait)
        _last[0] = time.time()


def call(params, tries=6):
    params = dict(params, format='json', maxlag=5)
    for i in range(tries):
        _throttle()
        try:
            r = S.get(API, params=params, timeout=30)
            if r.status_code == 429 or r.status_code >= 500:
                time.sleep(float(r.headers.get('Retry-After') or (3 + 4 * i))); continue
            j = r.json()
            if j.get('error', {}).get('code') == 'maxlag':
                time.sleep(5); continue
            return j
        except Exception:
            time.sleep(2 + 3 * i)
    return {}


def sparql(q, tries=5):
    for i in range(tries):
        _throttle()
        try:
            r = S.post(SPARQL, data={'query': q}, headers={'Accept': 'application/sparql-results+json'}, timeout=90)
            if r.status_code == 429 or r.status_code >= 500:
                time.sleep(float(r.headers.get('Retry-After') or (5 + 5 * i))); continue
            return r.json()['results']['bindings']
        except Exception:
            time.sleep(3 + 4 * i)
    return []


_search_info = {}  # qid -> (label, description) from search results
def search(text, lang='en', limit=6):
    if not text: return []
    j = call(dict(action='wbsearchentities', search=text, language=lang, uselang='en', limit=limit, type='item'))
    ids = []
    for x in j.get('search', []):
        ids.append(x['id']); _search_info.setdefault(x['id'], (x.get('label', ''), x.get('description', '')))
    if len(ids) < 2:  # fall back to full-text search (finds 'Treaty of Fez' etc.)
        j = call(dict(action='query', list='search', srsearch=text, srlimit=limit, srnamespace=0))
        ids += [x['title'] for x in (j.get('query') or {}).get('search', []) if re.match(r'Q\d+$', x['title'])]
    return list(dict.fromkeys(ids))


_info = {}
def details(ids):
    """Batched SPARQL: labels, description, types, life/period years, coords, sitelinks, aliases."""
    need = [q for q in dict.fromkeys(ids) if q not in _info]
    for k in range(0, len(need), 120):
        chunk = need[k:k + 120]
        q = """SELECT ?item ?en ?he ?yi ?desc ?sl ?coord
          (GROUP_CONCAT(DISTINCT ?tl; separator="|") AS ?types)
          (GROUP_CONCAT(DISTINCT ?al; separator="|") AS ?aliases)
          (MIN(YEAR(?b)) AS ?born) (MIN(YEAR(?d)) AS ?died) (MIN(YEAR(?s)) AS ?start) (MIN(YEAR(?e)) AS ?end)
          (SAMPLE(?h) AS ?human) WHERE {
          VALUES ?item { %s }
          OPTIONAL { ?item rdfs:label ?en FILTER(LANG(?en)="en") }
          OPTIONAL { ?item rdfs:label ?he FILTER(LANG(?he)="he") }
          OPTIONAL { ?item rdfs:label ?yi FILTER(LANG(?yi)="yi") }
          OPTIONAL { ?item schema:description ?desc FILTER(LANG(?desc)="en") }
          OPTIONAL { ?item wikibase:sitelinks ?sl }
          OPTIONAL { ?item wdt:P625 ?coord }
          OPTIONAL { ?item wdt:P31 ?t . ?t rdfs:label ?tl FILTER(LANG(?tl)="en") }
          OPTIONAL { ?item wdt:P31 wd:Q5 . BIND(1 AS ?h) }
          OPTIONAL { ?item skos:altLabel ?al FILTER(LANG(?al)="en") }
          OPTIONAL { ?item wdt:P569 ?b } OPTIONAL { ?item wdt:P570 ?d }
          OPTIONAL { ?item wdt:P580|wdt:P571|wdt:P585 ?s } OPTIONAL { ?item wdt:P582|wdt:P576 ?e }
        } GROUP BY ?item ?en ?he ?yi ?desc ?sl ?coord""" % ' '.join('wd:' + x for x in chunk)
        for b in sparql(q):
            qid = b['item']['value'].rsplit('/', 1)[1]
            g = lambda k: b.get(k, {}).get('value', '')
            num = lambda k: int(float(g(k))) if g(k) else None
            if qid in _info: continue
            _info[qid] = dict(qid=qid, en=g('en'), he=g('he'), yi=g('yi'), desc=g('desc'),
                              types=[x for x in g('types').split('|') if x][:4], is_human=bool(g('human')),
                              coords=bool(g('coord')), born=num('born'), died=num('died'), start=num('start'), end=num('end'),
                              aliases_en=[x for x in g('aliases').split('|') if x][:8], sitelinks=num('sl') or 0)
    return _info


PLACE_HINT = re.compile(r'city|town|village|country|state|region|province|capital|island|river|sea|mountain|port|district|municipality|kingdom|empire|neighbo|quarter|oasis|territory|colony|protectorate|settlement|commune|county|governorate|vilayet|sanjak|street|square|lake|bay|strait|peninsula|continent|desert|area|ghetto|place|location|historical country|sultanate|emirate|duchy|monarchy', re.I)
ORG_HINT = re.compile(r'organi|party|parliament|council|ministry|company|bank|society|newspaper|school|institution|agency|army|navy|court|government|legislat|assembly|committee|union|association|church|order|movement|military|police|university|congress|club|federation|fund|periodical|news', re.I)


def type_ok(typ, c):
    if typ == 'ppl': return c['is_human'] and (c['born'] is None or c['born'] < 1905) and (c['died'] is None or c['died'] > 1840)
    if typ == 'pl': return c['coords'] or any(PLACE_HINT.search(x) for x in c['types'])
    if typ == 'org': return not c['is_human'] and (any(ORG_HINT.search(x) for x in c['types']) or not c['coords'])
    return not c['is_human']


SKIP = re.compile(r'unidentified|fictional|named in|person in .*telegram|unknown|unnamed|generic', re.I)
def skip_lookup(ent):
    return ent.get('no_wd') or SKIP.search((ent.get('en') or '') + ' ' + (ent.get('desc') or '') + ' ' + (ent.get('kind') or ''))

def candidates_for(ent):
    ids = []
    names = [ent['en']] if ent.get('en') else []
    names += ent.get('en_alt', []) or []
    for n in names:
        ids += search(n, 'en', 6)
    hit = any(_search_info.get(q, ('', ''))[0].lower() in {x.lower() for x in names} for q in ids)
    if not hit and ent.get('he'):          # Hebrew search only when English found no exact label
        ids += search(ent['he'], 'he', 4)
    return list(dict.fromkeys(ids))[:10]


def rank(ent, ids):
    typ = ent['id'].split(':')[0]
    en = (ent.get('en') or '').lower().strip()
    alts = {x.lower() for x in ent.get('en_alt', []) or []}
    out = []
    for q in ids:
        c = _info.get(q)
        if not c:
            lab, desc = _search_info.get(q, ('', ''))
            c = dict(qid=q, en=lab, he='', yi='', desc=desc, types=[], is_human=False, coords=False, born=None, died=None, start=None, end=None, aliases_en=[], sitelinks=0)
        c = dict(c)
        names_c = {c['en'].lower()} | {a.lower() for a in c['aliases_en']}
        c['name_match'] = bool(names_c & ({en} | alts))
        c['type_ok'] = type_ok(typ, c)
        out.append(c)
    good = sorted([c for c in out if c['name_match'] and c['type_ok']], key=lambda c: -c['sitelinks'])
    auto = None
    if len(good) == 1 or (len(good) > 1 and good[0]['sitelinks'] >= 3 * max(1, good[1]['sitelinks'])):
        auto = good[0]['qid']
    return out, auto


def cmd_candidates(paths, only_missing=False, threads=3):
    for path in paths:
        data = json.load(open(path, encoding='utf-8'))
        ents = data.get('entities') or data.get('events', [])
        todo = [e for e in ents if not (only_missing and 'qid' in e) and not skip_lookup(e) and (e.get('en') or e.get('he'))]
        print(f'{path}: searching {len(todo)} of {len(ents)} entities', file=sys.stderr, flush=True)
        found = []
        with ThreadPoolExecutor(threads) as ex:
            for i, r in enumerate(ex.map(candidates_for, todo)):
                found.append(r)
                if i % 100 == 0: print(f'  {i}/{len(todo)}', file=sys.stderr, flush=True)
        details([q for ids in found for q in ids])
        cand_path = re.sub(r'\.json$', '.cand.json', path)
        old = json.load(open(cand_path, encoding='utf-8')) if os.path.exists(cand_path) else {}
        keep = ('qid', 'en', 'he', 'desc', 'types', 'born', 'died', 'start', 'end', 'sitelinks', 'name_match', 'type_ok')
        n_auto = 0
        for e, ids in zip(todo, found):
            cands, auto = rank(e, ids)
            old[e['id']] = [{k: c[k] for k in keep} for c in cands]
            e['qid_auto'] = auto; n_auto += bool(auto)
        json.dump(data, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        json.dump(old, open(cand_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print(f'{path}: {len(todo)} looked up, {n_auto} auto-matched -> {cand_path}', file=sys.stderr, flush=True)


def fmt(c):
    life = f" ({c['born'] or '?'}–{c['died'] or '?'})" if c.get('is_human') else (f" [{c['start'] or ''}–{c['end'] or ''}]" if c.get('start') or c.get('end') else '')
    return f"{c['qid']}\t{c['en']} / {c['he']}{life}\t{c['desc']}\t<{', '.join(c['types'])}>\tsl={c['sitelinks']}"


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'): sys.stdout.reconfigure(encoding='utf-8')
    cmd, args = sys.argv[1], sys.argv[2:]
    if cmd == 'search':
        res = []
        for n in args:
            lang = 'he' if re.search(r'[֐-׿]', n) else 'en'
            res.append((n, search(n, lang, 6)))
        details([q for _, ids in res for q in ids])
        for n, ids in res:
            print('##', n)
            for q in ids:
                if q in _info: print('  ' + fmt(_info[q]))
    elif cmd == 'get':
        details(args)
        for q in args: print(fmt(_info[q]) if q in _info else q + '\t(missing)')
    elif cmd == 'candidates':
        cmd_candidates([a for a in args if not a.startswith('--')], '--only-missing' in args)


# ---------------- batched search through the query service (avoids API rate limits) ----------------
def _lit(s):
    return '"' + s.replace(chr(92), chr(92) * 2).replace('"', chr(92) + '"') + '"'


def search_many(terms, lang='en', limit=6, chunk=40):
    """{term: [qids]} using the WDQS mwapi EntitySearch service, many terms per request."""
    out = {t: [] for t in terms}
    terms = [t for t in dict.fromkeys(terms) if t and t.strip()]
    for k in range(0, len(terms), chunk):
        part = terms[k:k + chunk]
        q = """SELECT ?term ?item ?num WHERE { VALUES ?term { %s }
          SERVICE wikibase:mwapi { bd:serviceParam wikibase:endpoint "www.wikidata.org"; wikibase:api "EntitySearch";
            mwapi:search ?term; mwapi:language "%s". ?item wikibase:apiOutputItem mwapi:item. ?num wikibase:apiOrdinal true. }
          FILTER(?num < %d) }""" % (' '.join(_lit(t) for t in part), lang, limit)
        rows = sparql(q)
        res = {}
        for r in rows:
            res.setdefault(r['term']['value'], []).append((int(r['num']['value']), r['item']['value'].rsplit('/', 1)[1]))
        for t, l in res.items():
            out[t] = [x for _, x in sorted(l)]
        print(f'    search[{lang}] {min(k + chunk, len(terms))}/{len(terms)}', file=sys.stderr, flush=True)
    return out


def cmd_candidates_batched(paths, only_missing=False):
    files = []
    for path in paths:
        data = json.load(open(path, encoding='utf-8'))
        ents = data.get('entities') or data.get('events', [])
        todo = [e for e in ents if not (only_missing and 'qid' in e) and not skip_lookup(e) and (e.get('en') or e.get('he'))]
        files.append((path, data, ents, todo))
        print(f'{path}: {len(todo)} of {len(ents)} to look up', file=sys.stderr, flush=True)
    allt = [e for _, _, _, todo in files for e in todo]
    en_names = lambda e: [x for x in [e.get('en')] + list(e.get('en_alt') or []) if x]
    r_en = search_many([n for e in allt for n in en_names(e)], 'en')
    ids_of = {e['id']: list(dict.fromkeys(q for n in en_names(e) for q in r_en.get(n, []))) for e in allt}
    details([q for v in ids_of.values() for q in v])
    def exact(e):
        names = {x.lower() for x in en_names(e)}
        return any(({(_info.get(q) or {}).get('en', '').lower()} | {a.lower() for a in (_info.get(q) or {}).get('aliases_en', [])}) & names for q in ids_of[e['id']])
    need_he = [e for e in allt if e.get('he') and not exact(e)]
    print(f'hebrew fallback for {len(need_he)}', file=sys.stderr, flush=True)
    r_he = search_many([e['he'] for e in need_he], 'he', 4)
    for e in need_he:
        ids_of[e['id']] = list(dict.fromkeys(ids_of[e['id']] + r_he.get(e['he'], [])))[:10]
    details([q for v in ids_of.values() for q in v])
    keep = ('qid', 'en', 'he', 'desc', 'types', 'born', 'died', 'start', 'end', 'sitelinks', 'name_match', 'type_ok')
    for path, data, ents, todo in files:
        cand_path = re.sub(r'\.json$', '.cand.json', path)
        old = json.load(open(cand_path, encoding='utf-8')) if os.path.exists(cand_path) else {}
        n_auto = 0
        for e in todo:
            cands, auto = rank(e, ids_of[e['id']])
            old[e['id']] = [{k: c[k] for k in keep} for c in cands]
            e['qid_auto'] = auto; n_auto += bool(auto)
        json.dump(data, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        json.dump(old, open(cand_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print(f'{path}: {len(todo)} looked up, {n_auto} auto-matched -> {cand_path}', file=sys.stderr, flush=True)


if __name__ == '__main__' and sys.argv[1] == 'candidates2':
    cmd_candidates_batched([a for a in sys.argv[2:] if not a.startswith('--')], '--only-missing' in sys.argv)
