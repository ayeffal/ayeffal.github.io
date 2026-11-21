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
