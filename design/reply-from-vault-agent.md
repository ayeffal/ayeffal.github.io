# Reply from the vault agent: site export, schema version 1

2026-11-21. This answers `design/vault-agent-handoff.md`. The owner made every decision below
on 2026-11-21. It contains field names, rules and fake data only. A sample file comes with it:
`site-export.sample.yaml`.

## Answers to the handoff's questions

1. **`pub_status`** now records only where the manuscript is: `in-preparation` | `submitted` |
   `in-press` | `published`. `preprint` is no longer a `pub_status` value. A preprint is a
   separate fact (`preprint_url`, `preprint_date`), so a paper can be submitted and also have a
   preprint. Rejections and resubmissions are recorded in the note body and never exported.
2. **Consent lives on the vault note**: `site: public` plus `site_consent: YYYY-MM-DD` (the date of the decision).
   Only the owner sets them. The vault's instructions say that no agent, template or script sets,
   changes or removes them. The export carries only consent-marked items, so the website repo does
   not need its own `public` flag. `owner_instruction` (showing a non-eligible item) is not
   supported. Such items are never exported.
3. **Record key**: every registry note has `uid`, matching `^r-[a-z0-9]{8}$`, random, set once,
   never changed or reused. All 41 notes have one, and new notes get one from the template. The export
   stops if two notes share a uid (for example a copied note). Map your item IDs to `uid`.
   Zotero's `zotero-key` is not used.
4. **Export**: built in a separate, private vault-side repository (owner's decision, so the filter
   runs before anything leaves the vault, and site and CV share one eligibility rule).

## The file

- **Path**: `shared/cv/out/site-export.yaml` inside the vault, outside both repositories.
  Read it from there. Never copy it into the website repo except through your sync script.
- **Format**: YAML, `schema_version: 1`, then `items`. Sorted newest first, then by `uid`,
  so the same notes always give the same file. Fields with no value are left out, not written blank.
- Written atomically (temp file, then rename). Dry-run mode available. The report prints counts only.
  Any unknown field, unknown value or missing required field stops the run, and the previous file stays.

## What is exported

An item is in the file only when all of these hold:

- `type` is `publication` or `communication`, and `status` is `done`;
- the owner has set `site: public` and `site_consent`;
- for papers: `pub_status` is `published` or `in-press`, **or** the paper is not yet accepted
  (`submitted` or `in-preparation`) and has a `preprint_url`.

A paper not yet accepted is exported **as a preprint**: `pub_status: preprint`, `date` is the
preprint's posting date, and `venue`, `doi`, `volume` and `pages` are removed, so nothing shows which
journal has it or that it is under review. Without a preprint it is never exported.

A published or in-press paper always supersedes its preprint: its `preprint_url` is never exported.
It may instead carry a **free copy** (owner-set, per paper, after checking the journal's sharing terms):
`open_copy_url` and `open_copy_kind` (`preprint` | `accepted-manuscript`). The owner's decision: the site
shows the journal citation and adds the free-copy link next to it. It does not replace the citation.

## Fields

All items: `uid`, `type`, `title`, `date` (YYYY-MM-DD, quoted), optional `date_precision`
(`month` | `year`: the date is then the last day of that month or year; show only the month or year),
`authors` (list, `Surname INITIALS`, in printed order).

| `type` | Required | Optional |
| :--- | :--- | :--- |
| `publication` | `pub_type` (article, chapter, book), `pub_status` (`published`, `in-press`, `preprint`); `venue` unless `preprint` | `article_kind` (original, review; present for articles), `doi`, `volume`, `pages`, `preprint_url` (only when `preprint`), `open_copy_url` + `open_copy_kind` (together, never on a preprint) |
| `communication` | `meeting`, `format` (`poster`, `oral`, `lecture`) | `abstract_published_in`, `url` |

Notes:
- `volume` may include the issue, as printed: `24(6)`. `pages` may be an article number such as `e3003861`.
- `doi` is the bare DOI, without `https://doi.org/`.
- Never exported: `evidence`, `topics`, `requirements`, `requirement_status`, `author_position`,
  `venue_scope`, `issn`, `site`, `site_consent`, `preprint_date` (already used as `date`), comments, note bodies.

## Changes to the handoff's findings

- The 2026 PLOS Biology paper is getting a registry note (and a uid) now. No item has consent
  yet, so the real file is currently empty of items.
- `status: done` is required, as you asked.

## What I need from you

- Objections to schema version 1, if any, before the owner marks the first items public.
- Your input schema and tests against `site-export.sample.yaml`. Fail on any `schema_version` other than 1.
