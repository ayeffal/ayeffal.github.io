# 0004. Data schema and public allowlist

Status: accepted, 2026-11-21 (see Open points)

## Context

The vault is the source of truth but is read-only, private and still
changing in structure. Only fields on an explicit public allowlist may be
copied into this repo (CLAUDE.md, Privacy). Pages for papers, talks and posters need more
than a citation.

## Decision

Three layers, each with its own home:

1. **Bibliographic fields, copied from the vault** through its export
   (0008). Only these may be copied:
   - all item types: `uid`, `title`, `date`, `date_precision`, `authors`
   - papers: `pub_type`, `article_kind`, `pub_status`, `venue`, `doi`,
     `volume`, `pages`, `preprint_url`, `open_copy_url`, `open_copy_kind`
     (`open_copy_url` is an external link to a free copy, never a hosted
     file; it is shown next to the journal citation, not instead of it)
   - talks and posters: `meeting`, `format`, `abstract_published_in`, `url`
     (the vault's `url` field already means "public page of the abstract or
     programme")
2. **Authored text, written in this repo**, one short file per item:
   an abstract or short summary in the owner's own words. This text is not
   copied from the vault.
3. **Site-only fields, in this repo**: `id` (0003), `related` (links to other
   items), and any `files` entries.

Never copied: `evidence`, `topics`, `requirements`, `requirement_status`,
`author_position`, `venue_scope`, `issn`, `site`, `site_consent`,
`preprint_date`, inline comments in the front matter, and note bodies.

Visibility: an item is public only when two things hold: the owner has set
consent on the vault note (so the vault's export contains it, 0008), and the
manifest has an entry for it (0003). A vault `pub_status` of `published` never
makes an item public by itself. Unpublished manuscripts follow 0002. Changed
2026-11-21: the site no longer has its own `public` flag.

Files:
- Small final-form files (poster PDFs, slides, a paper PDF the owner has the
  right to share) may live in the repo, a few MB each, with PDF metadata
  stripped before commit.
- Large files and recordings are external links, on a service with permanent
  URLs.
- Nothing is added to the repo until the owner names it explicitly. Git
  history keeps deleted files, so an upload cannot be fully undone.
- Paper PDFs need a rights check per item. Poster and slide files need
  co-author consent. License terms are set in 0007.

## Alternatives

- Copy all vault fields and filter at render time: rejected, because the
  repo history would then hold private data.
- Use vault `pub_status` as the visibility switch: rejected, because it
  cannot express "published but not approved for the site".
- Link every file to personal cloud storage: rejected, because links break
  and the permanence goal fails. Allowed only for large files.
- Copy publisher abstracts: not the default, because rights differ by
  publisher. A summary in the owner's words avoids the question.

## Consequences

- Each item needs a manual authored text file, which adds to the
  under-10-minutes goal.
- Changing the allowlist later is easy to widen and slow to narrow, because
  data already committed stays in history.
- The CLAUDE.md "Pending setup" hookify rule must check for fields not on
  this list.

## Confirmed 2026-11-21

- Author names appear as the vault stores them (surname and initials).
- Papers point to the publisher's version through the DOI. A hosted PDF is
  optional, shown only as a small link or icon, and only when the owner has
  the right to share it. For other papers, readers can ask the owner.

## Open points

- Whether `author_position` should appear on pages (excluded for now).
