# -*- coding: utf-8 -*-
"""Shared helpers for the knowledge-base (KB) pipeline."""
import re, os, json

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
KB = os.path.join(ROOT, 'kb')
WORK = os.path.join(KB, 'work')
TYPES = ('ppl', 'pl', 'org', 'grp', 'top')
TYPE_NAMES = {'ppl': 'person', 'pl': 'place', 'org': 'organization', 'grp': 'population group', 'top': 'topic', 'ev': 'event'}


def split_item(s):
    """'עברית (יידיש)' -> [he, yi]"""
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
    """Surface-form key (same as the site's H.nk)."""
    h = re.sub(r'[׳״"\'`’‘“”]', '', h)
    h = h.replace('־', ' ').replace('-', ' ')
    h = re.sub(r'\s+', ' ', h).strip()
    if len(h) > 3 and h[0] == 'ה': h = h[1:]
    return h


def load_json(p, default=None):
    if not os.path.exists(p): return default
    with open(p, encoding='utf-8') as f: return json.load(f)


def save_json(p, obj, compact=False):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w', encoding='utf-8') as f:
        if compact: json.dump(obj, f, ensure_ascii=False, separators=(',', ':'))
        else: json.dump(obj, f, ensure_ascii=False, indent=1)
