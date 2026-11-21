# Academic website

* **Author:** Abraham Yeffal
* **Date:** 2026-11-21

## Overview

A personal academic website on GitHub Pages for a PhD candidate in
neuroscience in Argentina. It has five pages: Home, Research, Papers, Talks
and posters, and a public CV. A private notes vault is the source of truth.
A program in the vault repo writes one export file with only the items the
owner approved for the site. A local script, `sync`, reads that file and
writes committed data files. An automatic build, `build`, turns those files
into pages with Quarto. The build never sees the vault.

Papers, talks and posters can have their own permanent page at
`/<type>/<id>/`. A page exists only when the item has a summary written by
the owner or a hosted file. Otherwise the item is a row in a list that links
to the publisher. The site is English-only, with `/es/` reserved.

The decisions behind this are in `docs/decisions/` (0001 to 0010). This brief
summarises them and records what the Goldfish review found and what is still
open.

## Analysis

The Goldfish review (seven lenses) read decisions 0001 to 0007 and raised nine
main objections. Status of each after decisions 0008 to 0010:

| # | Objection | Status |
| --- | --- | --- |
| 1 | Privacy rested on a local hook. | **Addressed in 0009**: allowlist as a schema that rejects extra keys, plus a scan for paths, usernames and DNI/CUIL, run before each commit and again in the automatic build. **Not built yet.** |
| 2 | The copy step was not gated by approval. | **Addressed in 0003, 0008, 0009**: only items the owner marks as public are exported, and only allowlisted fields. Needs the vault agent's agreement. |
| 3 | The pipeline was described inconsistently. | **Addressed in 0009**: `sync` (local, reads the export) and `build` (automatic, reads committed files). |
| 4 | The untracked ID-to-vault link file. | **Resolved in 0003**: the link lives in the tracked manifest for public items only. A stable record key (proposed: ZotLit's `zotero-key`) avoids using titles. |
| 5 | Permanence and takedown. | **Addressed in 0009**: ledger of released URLs, append-only manifest, tombstone pages, history rewrite only for a privacy leak with the owner's approval. Not built. |
| 6 | One registry for both site and CV. | **Resolved in 0008**: same item list for papers, talks and posters. The CV may add other item types and has two contact variants (public and individual). |
| 7 | The ten-minute goal is untested. | **Open.** No walkthrough exists. Best written after a few real items. |
| 8 | No findability work. | **Partly addressed**: five pages, ORCID and Google Scholar links, citation meta tags and a sitemap (0009, 0010). Not built. Search Console registration is undecided. |
| 9 | Quarto size and untested CI and PDF. | **Partly tested**: `/papers/<id>/` URLs and a list mixing external and internal links work (Quarto 1.11.9, fake data). PDF output, a CI build and a real icon are not tested. |

Other points from the review:

- **Hosting PDFs in git cannot be undone.** 0004 and 0009 limit it to small
  final-form files (5 MB cap, metadata stripped, rights and co-author checks)
  and nothing goes in until the owner names it. Zenodo for larger files
  remains an option.
- **Two visibility controls.** 0009 settles it: a hand-set `public` flag, plus
  an `owner_instruction` field with the owner's exact words for anything not
  eligible.
- **Quarto redirects (`aliases:`)** might soften the "no redirects" premise.
  Not verified.
- **Co-author names are third-party data.** No removal procedure is written.
- **A summary that paraphrases a publisher abstract** might carry third-party
  rights, and CC BY 4.0 cannot be withdrawn. 0004 says summaries are in the
  owner's words, but a rule for checking this is not written.

Findings from the vault itself (a field-only check of 41 registry notes):
two publications, both published; eleven communications, all with a `format`;
no submitted, preprint or in-press items yet. The owner's 2026 co-authored
paper (PLOS Biology) has no registry note in `shared/registry`.

## Goals vs. Non-Goals

* **In-Scope Goals:**
  * A findable, credible academic home (five pages, ORCID, Scholar).
  * The same registry notes feed the site and the PDF CV, through one export
    and two contact variants.
  * Zero cost and no lock-in: plain files, Quarto pinned, rebuildable from a
    clone.
  * Private by construction: allowlist as a schema, scans before commit and
    in the automatic build, unpublished work excluded by default.
  * Adding an item in under 10 minutes (goal, not yet shown).
* **Out-of-Scope Non-Goals:** Blog, analytics, trackers, comments, forms,
  custom domain, a contact form, Spanish pages (for now), pages for courses,
  awards, software or datasets, teaching and news pages.

## Alternatives Weighed

- **Bilingual from day one**: rejected. It doubles the work and no Spanish
  need exists in the next year (0001).
- **English under `/en/`**: rejected. It would make later moves break links.
- **Item pages for every type or every item**: rejected. Pages with almost no
  content look worse than a list row (0002).
- **List pages only, with anchors**: rejected. Anchors are not permanent
  addresses.
- **DOI, opaque or title-based IDs**: rejected. A readable
  `surname-year-tag` is kept (0003).
- **Hugo**: rejected for Quarto, because Go templates are harder for the owner
  to maintain. Python-rendered HTML was suggested as a lighter option and was
  not adopted (0006).
- **Jekyll**: rejected. It needs Ruby and cannot make PDFs.
- **A wider CV allowlist**: dropped. The owner will not list in-review or
  in-preparation work on any CV (0008).
- **A contact form**: rejected. Forms are a non-goal, they need a third-party
  service and they still receive spam. The email is shown as
  `name (at) domain (dot) tld` (0008).
- **English-first affiliation with the Spanish original in parentheses, or
  Spanish-first with English in parentheses**: English-first kept, matching
  the owner's PLOS paper and the supervisor's CV. Spanish official names sit
  in page metadata (0010). A Spanish-first rule from a research file could not
  be verified.
- **Consent kept only in the website repo**: still open. The vault agent may
  instead hold a consent field.

## Key Decisions & Staging for Next Steps

Decided (see `docs/decisions/`): 0001 language, 0002 URLs, 0003 IDs, 0004
schema and allowlist, 0005 display name, 0006 Quarto, 0007 licenses, 0008 CV
source, 0009 privacy and permanence, 0010 pages and affiliation.

Still open:

1. **Vault agent**: consent field in the vault or the website repo, who
   creates stable record keys, and the export format.
   `design/vault-agent-handoff.md` is the input. The vault repo has no export
   yet.
2. **Building**: the allowlist schema and privacy scans must exist before the
   first commit of generated data (CLAUDE.md pending setup).
3. **Untested**: a CI build with pinned Quarto, PDF output and an icon for
   rows with a page.
4. **Not written**: the ten-minute walkthrough, a lifecycle table (a preprint
   gains a DOI, a page loses its summary, a related item is not public), error
   messages, a glossary, a repo layout, `LICENSE` and the content notice, and
   a co-author removal procedure.
5. **Text and metadata**: the owner's Methods line, Search Console
   registration, and a note for the owner's 2026 paper in the vault.
6. **Housekeeping**: the stale "decision 3" and "decision 6" references in
   0001, 0002 and 0004 now use file numbers (fixed 2026-11-21). 0004 is marked
   accepted with one open point (`author_position`).

Staging: papers first would be the smallest start. Talks, posters and
`related` links need the same machinery and can follow. The pending setup in
CLAUDE.md (frontend-design, modern-web-guidance, Playwright, then
claude-code-setup, then the add-item skill) follows design approval and the
scaffold.

## Not checked

No reviewer inspected the vault, Quarto's behaviour beyond the fake-data test,
CI, or any code (none exists). Claims about GitHub Pages limits, Quarto
`aliases:` and CONICET's affiliation rule for websites are from general
knowledge or partial reading. UBA's affiliation resolution could not be read.
