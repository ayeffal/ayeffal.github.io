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
  registry note in `shared/registry`. It may be elsewhere, for example the
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

## What the website repo needs next from you

- Agreement or objections on questions 1 to 3.
- The export's path and a sample with fake data, so the website repo can
  write its input schema and tests.

## Not decided

- Where the export is stored, and its exact name and schema.
- Whether consent lives in the vault or the website repo.
- Who creates the record keys.
