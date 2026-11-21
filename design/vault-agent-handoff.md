# Handoff for the vault-repo agent: site export, consent flag, pub_status

Updated 2026-11-21 by the agent working on the website repo, after decisions
0001 to 0010 in that repo's `docs/decisions/`. It lists what the website repo
needs from the vault repo. It contains field names and rules only, no note
content. Nothing here is final until the owner says so. The owner has not
yet agreed to any item in the "Questions" section; those are proposals.

## Background

The website repo is public. The vault is private, and read-only for the
website agent. The vault repo has no export yet.

Settled in the website repo (owner decisions):

- The site shows papers, talks and posters. Courses, awards and teaching are
  not shown.
- **Eligible statuses**: published, in press, preprint. Work in preparation,
  submitted (in review) and drafts are never shown, on the site or on any CV,
  unless the owner gives an explicit instruction naming that item.
- Eligible does not mean public. An item becomes public only through an
  explicit consent action by the owner. Agents never set it.
- The vault repo builds the CV. This repo's site reads only a file the vault
  repo writes, so only the vault repo knows the vault's layout.
- Same item list for site and CV (papers, talks, posters). The CV may add
  other item types (degrees, positions, teaching, courses).
- Two CV variants differing only in the contact block. The individual one
  (phone, direct email, perhaps address) takes its contact details from a
  local file kept outside both repos. Neither variant includes DNI/CUIL.

## Questions for the owner and the vault agent

### 1. `pub_status`

Today one value from: published | in-press | submitted | preprint.

- One value cannot say "submitted and also on a preprint server".
- There is no value for "in preparation" or "draft".
- It is a fact about the paper, not a statement of consent.

Proposal: add `in-preparation`. Keep any preprint link in a separate field
(for example `preprint_url`), so a manuscript can stay `submitted` and still
have a preprint. Eligibility is then computed from `pub_status` plus the
presence of that link. Decision for the owner: whether a submitted manuscript
with a preprint counts as eligible. (Their stated rule: preprints are
eligible.)

**Settled 2026-11-21.** `pub_status` is `in-preparation` | `submitted` |
`in-press` | `published`; `preprint` is no longer a value. The preprint link is
`preprint_url`. A submitted or in-preparation paper with a `preprint_url` is
exported as a preprint, with `venue`, `doi`, `volume` and `pages` removed.
Without a preprint it is never exported.

### 2. A consent field in the vault

Proposal: one field, for example `site: public`. Absent or any other value
means not public. Only the owner sets it, with the date and the owner's exact
words in an adjacent comment. No agent, bulk rename or normalising script
sets or changes it. If this is adopted, the vault agent's own instructions
must say so.

Alternative: leave consent in the website repo's manifest (a hand-set `public`
flag there), and the export carries every eligible item. Decision for the
owner. Preferred by the website agent: the vault field, so there is one place.
Risk: any script rewriting front matter can change it by accident.

**Settled 2026-11-21 (consent only).** Consent lives on the vault note:
`site: public` plus `site_consent: YYYY-MM-DD`, set only by the owner. The
export carries only consent-marked items. The vault agent does not support
`owner_instruction`: such items are never exported. Whether this repo still
needs its own `public` flag, and what happens to `owner_instruction` in
decisions 0002, 0004 and 0009, is **open** (see the list at the end).

For an item that is not eligible (submitted, in preparation, draft), the
website repo requires an additional `owner_instruction` (date plus the
owner's exact words) before it can appear. Whether this lives in the vault or
the website repo follows the same decision.

### 3. Stable record key and IDs

The website repo assigns permanent item IDs (`surname-year-tag`, set once).
Today the link between an ID and a vault note would be the note's filename or
title, which changes and is sensitive for unpublished work.

Request: every registry note gets a stable, opaque record key that never
changes (for example `uid`). The export carries it. The website repo's
manifest then maps `ID -> record key`, with no title in the link. Decision:
who creates the key. The website agent cannot write to the vault.

The IDs stay in the website repo either way, with a committed ledger of
released URLs, so a published item cannot disappear.

**Settled 2026-11-21.** Every registry note has `uid` (`^r-[a-z0-9]{8}$`,
random, set once, never reused). The vault agent created them; the export
stops on duplicates. Zotero's `zotero-key` is not used. The manifest maps
`ID -> uid`.

### 4. The site export file

Request: the vault repo writes one structured file (YAML or JSON) for the
site, to a path agreed with the owner and outside the website repo. It holds
only items that are both eligible and consent-marked (see 1 and 2), and only
the fields below. Unpublished titles never leave the vault.

Fields the site may read:

- All types: `title`, `date`, `date_precision` (where present), `authors`
  (list, in the form `Surname Initials`), record key.
- Papers (`type: publication`): `pub_type`, `article_kind`, `pub_status`,
  `venue`, `doi`, `volume`, `pages`.
- Talks and posters (`type: communication`): `meeting`, `format`,
  `abstract_published_in`, `url`. The `format` field (poster, oral, lecture)
  decides the site route (`/posters/` or `/talks/`), so it must always be
  filled for exported items.

Never in the site export: `evidence`, `topics`, `requirements`,
`requirement_status`, `author_position`, `venue_scope`, `issn`, inline
comments in front matter, and note bodies. The CV tool reads the vault
itself and does not use this file.

Required properties:

- A `schema_version`, so the website repo fails when the format changes.
- Atomic write (temp file, then rename).
- A report that prints counts only, never titles or values.
- A dry-run mode.
- Failure on an unknown or missing required field, rather than silently
  skipping or passing it through.

**Settled 2026-11-21.** The export is `shared/cv/out/site-export.yaml` in the
vault, built by a separate private vault-side repository. Field list, rules
and sample: `design/reply-from-vault-agent.md` and
`design/site-export.sample.yaml`. This repo's input schema and tests are in
`sync/`. The fields beyond the list above are `uid`, `preprint_url`,
`open_copy_url` and `open_copy_kind`.

## Findings from a field-only check of the registry (2026-11-21)

A script counted front-matter values in `shared/registry` (41 notes). It
printed only counts, no titles or bodies. It reads simple `key: value`
lines, so multi-line values and values after a comment may read as blank.

- Publications: 2, both `published`, `article`, `original`. No note uses
  `submitted`, `preprint` or `in-press` yet.
- Communications: 11 (posters 8, `oral` 1, `lecture` 2). All have `format`.
  Only 3 have `url`.
- `status` is a separate field from `pub_status`, with values `done`,
  `planned` and `unavailable`. **The site export must also require
  `status: done`**, so a planned or unavailable item is never exported.
- `date_precision` is in use (`month`, `year`), so the export must carry it.
- A paper the owner co-authored in 2026 (Learning engages transient and
  sustained cellular mechanisms in the human brain, PLOS Biology) has no
  registry note in `shared/registry` (the vault agent is creating one). It may be elsewhere, for example the
  `work/doctorate/archive` batches. It is the paper the home-page text cites,
  so it needs a note (with the stable record key) before it can be an item.

## What Zotero (ZotLit) can supply

The vault runs ZotLit 2.2.4 (from the plugin manifest). Facts below come from
ZotLit's public documentation and were partly read; the field list was read
verbatim, the details of attachments and related items were not. Nothing was
tested against the owner's library.

- **Record key (question 3).** ZotLit always writes `zotero-key` into a
  literature note (from the Zotero item key, unique within a library, stable
  across edits, changed if the item moves to another library). Proposal: use
  it as the record key for notes that come from Zotero. Do not use the
  Better BibTeX citation key, which can be regenerated. Notes with no Zotero
  item (some talks and posters) still need a key of the vault's own.
- **Fields available** in ZotLit's template data: item type, title, creators
  (in Zotero's order), date (year and month parsed, so partial dates can feed
  `date_precision`), DOI, ISSN, publication title (the `venue`), volume, issue,
  pages, language, URL. Registry notes store volume as `117(38)`; Zotero holds
  volume and issue separately.
- **Preprint hint.** `itemType` is `preprint` or `journalArticle`, a hint for
  `pub_status`. No separate preprint flag was found. `in-press` and
  `submitted` are not Zotero fields.
- **Related items.** Zotero's "Related" links are readable (one level, same
  library), so a preprint could be linked to its published version.
- **Not to export:** tags, collections, attachment paths, Zotero's `extra`,
  and abstracts (the site copies no publisher abstracts, decision 0004).
- **Consent stays out of Zotero.** The consent field must be a vault field
  the owner sets by hand. Do not store it in a Zotero tag.
- **No schedule.** Managed front matter is written when a ZotLit command runs
  or a note is created, so notes can drift out of date. The export should
  report the age of each record's last update, or the owner should refresh
  before exporting.

## Settled in the second round (2026-11-21)

Answers are in `design/reply-2-from-vault-agent.md`; owner decisions in
decisions 0002, 0003, 0004 and 0009.

- An empty export is `items: []`. Every value is a double-quoted string
  except `schema_version`. `article_kind` is required for articles and absent
  for chapters and books. Sort order is `date` descending, then `uid`.
- No export date and no per-record age: registry notes are hand-edited, so
  there is nothing to refresh. Use the file's modification time.
- Each run prints counts of items added, removed, changed and unchanged, by
  uid. A released item missing from the export is an error in `sync`.
- A preprint that is published keeps its `uid` and changes in place.
- `owner_instruction` is retired. The site has no `public` flag: an item
  appears when it is in the export and has a manifest entry.
- The allowlist gains `date_precision`, `uid`, `preprint_url`, `open_copy_url`
  and `open_copy_kind`. The free copy is an external link.
- The PLOS Biology note has a `uid`; it is not exported until the owner marks
  it public.

## Still open

- Nothing the vault agent needs to answer. Remaining work is in this repo:
  the `sync` script, the manifest and the privacy check.
