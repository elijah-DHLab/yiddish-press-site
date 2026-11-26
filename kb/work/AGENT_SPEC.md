# Entity resolution spec (Yiddish press KB)

Corpus: 598 Yiddish newspaper articles (Der Fraynd, Haynt, Unzer Leben), 1905–1917, heavily about Morocco,
Salonica/Damascus, the Ottoman Empire, Russia, Jews, the Balkans, WWI. An earlier LLM pass extracted entity
names per article in **Hebrew** (with the Yiddish spelling in parentheses). The same real-world entity appears
under many spellings ("פאס" / "פס" / "פז"), with/without titles ("הקייזר וילהלם" / "וילהלם השני" / "הקייזר"),
and some forms are ambiguous ("הסולטאן", "הקיסר", "המלך") and must be resolved per article.

Paths are relative to the repo root (the current working directory). Use `python` (3.14).

## Inputs
- `kb/work/batch_<type>_<n>.tsv` — your batch. Columns: `key  display  variants  yiddish  count  first  last  article_ids`.
  `key` is the normalized surface form (leading ה׳ removed, punctuation removed). **Every key must be accounted for.**
- `kb/work/mentions_<type>.tsv` — all keys of this type (other batches too) — useful to see the full picture.
- `kb/work/articles.jsonl` — every article (id, date, paper, summary, all entity lists).
- `python kb/scripts/ctx.py <type> "<key>" [--short]` — the articles containing a key, with summaries and co-entities.
- `python kb/scripts/ctx.py art <article_id>` — one article.
- `python kb/scripts/wd.py search "English name" ...` — live Wikidata lookup (use sparingly, batched names per call).

## Output: `kb/work/ent_<type>_<n>.json` (UTF-8, ensure_ascii=False)
```json
{
 "entities": [
  {"id": "pl:fez", "he": "פאס", "en": "Fez", "en_alt": ["Fes"], "desc": "city in Morocco",
   "kind": "city", "parent": "pl:morocco", "keys": ["פאס", "פס", "פז"]},
  {"id": "ppl:abd-al-hafid", "he": "מולאי עבד אל-חפיט", "en": "Abd al-Hafid of Morocco", "desc": "Sultan of Morocco 1908–1912",
   "role": "סולטאן מרוקו (1908–1912)", "country": "pl:morocco", "keys": ["מולאי חאפיד", "מולאי חפיד", "עבד אל חפיד"]}
 ],
 "contextual": [
  {"key": "סולטאן", "articles": {"dfr19050410-01.2.12": "ppl:abdelaziz-of-morocco", "unzerleben19100502-01.2.3": "ppl:mehmed-v", "xxx": null}}
 ],
 "drop": [{"key": "העיר", "why": "generic noun, not a named entity"}]
}
```
Rules:
1. **Cluster** all keys that denote the same real-world entity into one entity (`keys` = list of batch keys, exactly as in column 1).
   Look at `variants`, `yiddish`, dates and contexts. Also merge with obvious matches you see in `mentions_<type>.tsv`
   from other batches by using the **same id** (ids are merged across batches automatically).
2. **id**: `<type>:<slug>`; slug = the English Wikipedia article title, lowercased, ASCII only (strip diacritics),
   words joined by `-`, no parentheses/commas (e.g. `ppl:wilhelm-ii-german-emperor`, `ppl:nicholas-ii-of-russia`,
   `pl:thessaloniki`, `pl:ottoman-empire`, `org:state-duma`). If no Wikipedia article, a descriptive English slug.
   The id prefix may differ from the batch type when the extractor mis-typed (e.g. a "place" key that is really the
   organization "הדומה" → `org:state-duma`; a "person" that is really a group). Keep such keys but give them the right prefix.
   For type `grp` keep prefix `grp`. Events that sneak in (e.g. "ועידת אלחסיראס" as an organization) → prefix `ev:`.
3. **he** = the best standard modern Hebrew name (as on Hebrew Wikipedia when one exists). **en** = the English
   name as on English Wikipedia/Wikidata (this is used to search Wikidata — make it precise; `en_alt` for alternatives).
   **desc** = short English disambiguating description (dates, role, country).
4. **Ambiguous keys** ("סולטאן", "קיסר", "מלך", "נשיא", "שר החוץ", "הוד מלכותו", bare surnames shared by several people,
   "קמבון" = Jules or Paul Cambon) → `contextual`: map **every** article containing the key to an entity id
   (or `null` if unresolvable). Use the date + article summary (`ctx.py`). The target entities must exist
   (in your `entities` with appropriate keys, or another batch — then just reference the id; for well-known people
   you may create the entity in your file with `"keys": []`). Example: the Sultan of Morocco is Abdelaziz until
   Aug 1908, Abd al-Hafid until Aug 1912, then Yusef; the Ottoman sultan is Abdul Hamid II until Apr 1909, then Mehmed V.
5. **drop** only true non-entities (generic nouns like "העיר", "הממשלה" without referent, OCR garbage). Prefer to
   resolve generic-but-referential forms ("הממשלה הצרפתית" → `org:government-of-france`).
6. `parent` (places: the containing place — city → country/region, e.g. `pl:morocco`; groups: broader group, e.g.
   `grp:jews`; organizations: parent organization). `country` (people: the state they serve/belong to;
   organizations: their country). Use these core ids for countries so batches agree:
   `pl:morocco pl:france pl:germany pl:russian-empire pl:ottoman-empire pl:united-kingdom pl:spain pl:italy
   pl:austria-hungary pl:united-states pl:persia pl:japan pl:china pl:greece pl:bulgaria pl:serbia pl:romania
   pl:montenegro pl:albania pl:egypt pl:algeria pl:tunisia pl:libya pl:ottoman-palestine pl:syria pl:belgium
   pl:netherlands pl:portugal pl:switzerland pl:sweden pl:denmark pl:norway pl:poland pl:ukraine pl:lithuania
   pl:finland pl:caucasus pl:yemen pl:iraq pl:lebanon pl:tripolitania pl:crete pl:macedonia pl:bosnia-and-herzegovina`
   (historic states: Russia = `pl:russian-empire`, Germany = `pl:germany` for the German Empire.)
   `kind`: free short English word (city, country, region, river, quarter, sultan, minister, journalist, rabbi,
   party, newspaper, ministry, ethnic group, religious group, ...).
7. Do not invent Wikidata QIDs. (QIDs are added in a later step from real search results.)

Validate before finishing: `python kb/scripts/validate.py kb/work/ent_<type>_<n>.json kb/work/batch_<type>_<n>.tsv`
and fix until it prints OK. Write the JSON with a Python script (json.dump, ensure_ascii=False, indent=1) rather than
by hand if that is easier; build it incrementally (it is large).
