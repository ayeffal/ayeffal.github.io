# 0003. Item IDs

Status: accepted, 2026-11-21

## Context

Papers, talks and posters get their own permanent URL (0002). The ID is the
last path segment, so it can never change after publication. The vault is
read-only, so IDs cannot be stored in the vault notes. The vault's note
structure is still changing, so the site must not depend directly on vault
field names or filenames.

## Decision

- Format: `<first-author-surname>-<year>-<tag>`.
  - Surname: lowercase ASCII, accents removed.
  - Year: the year of the item's first public version on the site. It is a
    label, not a citation. The page shows the real dates.
  - Tag: one or two lowercase words chosen once by the owner, joined with
    hyphens.
  - Example shape: `surname-2020-hippocampal`.
- No type or status in the ID (no `-poster`, `-preprint`). The directory
  already gives the type. Status (preprint, published) changes while the item
  stays the same, so the page shows it.
- Unique within a type. The same ID may exist under two types. A poster that
  later becomes a paper is a new item with its own ID, linked as "related".
- An ID is assigned once and never regenerated, even if authors, year or
  title later change.
- IDs live in a manifest in this repo. The manifest also holds the link
  between each ID and its export record: the record's `uid`, an opaque key
  that never changes (changed 2026-11-21: it was an untracked local file,
  then a note filename or title). Only public items appear in the manifest. An unpublished item
  has no entry, so its title or filename never enters the repo. The automatic
  build can then read the whole link.
- The vault's export already uses the public field names (0008), so there is
  no mapping file. The input schema (`sync/export_schema.py`) takes its
  place. If the export format changes, `schema_version` changes and `sync`
  fails with an error. It never skips a field and publishes a partial page.
  Changed 2026-11-21.
- A preprint that is later published keeps its `uid`, so it keeps its ID and
  URL and is updated in place.

## Alternatives

- DOI as ID: rejected, because unpublished items and talks have none and the
  slash and dots make poor URLs.
- Opaque ID (`p7k2`): rejected, because it says nothing to a reader.
- Title slug: rejected, because titles change between preprint and journal.
- No year: rejected by the owner. Tags alone collide more often and say less.
- Type or status suffix: rejected, because the path already carries type and
  status can change.
- IDs unique across all types: rejected, because the path separates types.

## Consequences

- Each ID is invented by hand once per item. This adds a small step to the
  "add an item in under 10 minutes" goal.
- A year can look wrong after a preprint is later published. This is accepted.
- The manifest is tracked, so it needs the same privacy scan as the data
  files. A vault note's filename is its title, so adding an item to the
  manifest is the moment it becomes public.
