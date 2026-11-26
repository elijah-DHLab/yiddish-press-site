#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Wikidata-match review helper.

  python kb/scripts/review.py show  kb/work/ent_pl_1.json [--all] [--from N --to M]
        compact list: entity line, then its candidates (✓ = name matches, T = type plausible, * = auto pick)
        without --all, entities whose auto pick is unambiguous are listed briefly at the end
  python kb/scripts/review.py apply kb/work/ent_pl_1.json decisions.json [--accept-auto]
        decisions.json = {"pl:fez": "Q80985", "pl:foo": null, ...}; --accept-auto sets qid=qid_auto for entities
        not in decisions.json that have no qid yet; entities still undecided get qid=null.
  python kb/scripts/review.py stats kb/work/ent_pl_1.json
"""
import sys, os, json, re
if hasattr(sys.stdout, 'reconfigure'): sys.stdout.reconfigure(encoding='utf-8')
cmd, path = sys.argv[1], sys.argv[2]
data = json.load(open(path, encoding='utf-8'))
ents = data.get('entities') or data.get('events', [])
cand = json.load(open(re.sub(r'\.json$', '.cand.json', path), encoding='utf-8')) if os.path.exists(re.sub(r'\.json$', '.cand.json', path)) else {}


def cline(c, auto):
    life = f"{c.get('born') or ''}–{c.get('died') or ''}" if (c.get('born') or c.get('died')) else (f"[{c.get('start') or ''}–{c.get('end') or ''}]" if c.get('start') or c.get('end') else '')
    flag = ('*' if c['qid'] == auto else ' ') + ('✓' if c.get('name_match') else ' ') + ('T' if c.get('type_ok') else ' ')
    return f"   {flag} {c['qid']}  {c['en']} / {c.get('he') or ''} {life} | {c.get('desc', '')[:80]} <{', '.join(c.get('types', [])[:2])}> sl={c.get('sitelinks')}"


if cmd == 'show':
    a = sys.argv
    lo = int(a[a.index('--from') + 1]) if '--from' in a else 0
    hi = int(a[a.index('--to') + 1]) if '--to' in a else len(ents)
    easy = []
    for n, e in enumerate(ents[lo:hi], lo):
        cs = cand.get(e['id'], [])
        auto = e.get('qid_auto')
        if not cs and not auto: continue
        if '--all' not in a and auto and sum(1 for c in cs if c.get('name_match') and c.get('type_ok')) == 1:
            easy.append((n, e, auto, next(c for c in cs if c['qid'] == auto))); continue
        print(f"[{n}] {e['id']} | {e.get('he')} | {e.get('en')} | {e.get('desc', '')[:90]}" + (f"  (current qid={e['qid']})" if 'qid' in e else ''))
        for c in cs[:7]: print(cline(c, auto))
    if easy:
        print('\n--- unambiguous auto picks (check the description fits):')
        for n, e, auto, c in easy:
            print(f"[{n}] {e['id']} ({e.get('desc', '')[:50]}) -> {auto} {c['en']} | {c.get('desc', '')[:70]}")
elif cmd == 'apply':
    dec = json.load(open(sys.argv[3], encoding='utf-8')) if len(sys.argv) > 3 and not sys.argv[3].startswith('--') else {}
    ids = {e['id'] for e in ents}
    bad = [k for k in dec if k not in ids]
    if bad: print('unknown ids in decisions:', bad[:20])
    for e in ents:
        if e['id'] in dec:
            q = dec[e['id']]
            if q is not None and not re.match(r'^Q\d+$', str(q)): print('bad qid', e['id'], q); continue
            e['qid'] = q
        elif 'qid' not in e:
            e['qid'] = e.get('qid_auto') if '--accept-auto' in sys.argv else None
    json.dump(data, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('applied; qid set:', sum(1 for e in ents if e.get('qid')), '/', len(ents))
elif cmd == 'stats':
    print('entities', len(ents), 'with candidates', sum(1 for e in ents if cand.get(e['id'])),
          'auto', sum(1 for e in ents if e.get('qid_auto')), 'qid', sum(1 for e in ents if e.get('qid')))
