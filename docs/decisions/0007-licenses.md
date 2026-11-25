# 0007. Licenses

Status: accepted, 2026-11-21

## Context

The repo holds code (generator script, templates, workflow), the owner's
own text, and possibly files that belong to others (publisher PDFs, group
posters, co-authored slides). A repo with no license cannot legally be
reused. A license already given for a copy cannot be taken back.

## Decision

- **Code**: MIT License, copyright "Abraham Yeffal" (0005), year of first
  publication.
- **Authored content** (page text, summaries, abstracts written by the
  owner): Creative Commons Attribution 4.0 International (CC BY 4.0).
- **Third-party and shared material** (publisher PDFs, posters, slides with
  co-authors, recordings, logos, photos of other people) is not covered by
  either license. Each such file shows a one-line rights note naming who holds
  the rights, and is added only after the rights and co-author consent checks
  in 0004.
- **Summaries and abstracts (added 2026-11-24).** A publisher abstract is
  free to read but not free to reuse: it stays under publisher or author
  copyright unless the paper is CC BY (Crossref says the same of the
  abstracts it distributes). So the owner's summaries are written fresh, not
  reworded from the abstract, because CC BY 4.0 on a near-copy would license
  what is not the owner's and cannot be withdrawn. A CC BY paper may also
  show its real abstract, labelled with that license and its source, not
  with the site's. That abstract alone is enough for the item to get its own
  page (0002). A summary is optional and its absence blocks nothing.
- **Checking the abstract's license (added 2026-11-24).** When the owner adds
  an abstract, a local check asks the Crossref API for the paper's DOI and
  accepts it only if a license entry for the published version (or with an
  unspecified version) is a `creativecommons.org/licenses/by/` URL. It then
  records that URL, the DOI and the check date in the authored file (0004).
  The license is recorded once, at that moment, because publishers can
  change Crossref entries later. The automatic build makes no network call:
  it fails if a page shows an abstract whose file lacks these fields or
  whose recorded URL is not CC BY. Alternatives rejected: Unpaywall (needs an
  email in each request), a hand-typed field (nothing catches a mistake),
  and Zotero's free-text Rights field via ZotLit (inconsistent, and the
  registry notes are not ZotLit-managed).
- The site footer states the content license and links to it.
- Contact details are not covered by a license and are decided separately.

## Alternatives

- Apache-2.0 for code: rejected, because its patent grant matters little for
  a personal site script and MIT is shorter.
- No code license: rejected, because it blocks even harmless reuse.
- CC BY-NC-ND or all rights reserved for content: rejected by the owner, who
  wants text to be shareable with credit.

## Consequences

- Anyone may copy and adapt the code and the owner's text, with credit.
- A licence file for each (`LICENSE` for code, a content license notice) is
  still to be created at build time. It was not created now.
- Wrongly attributing a file to the owner's license is a rights error. The
  per-file note and the hookify rule (CLAUDE.md) should guard against it.
