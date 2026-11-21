# 0005. Display name

Status: accepted, 2026-11-21

## Context

The name appears in page titles, headers, the footer, search results and
citations. Search engines index it, and it should match the name on the
owner's papers so that publications are found together.

## Decision

- The display name is **Abraham Yeffal**, the form used on the owner's papers.
- Formal documents use this form for now.
- Other name parts the owner has are not published on the site. They are not
  recorded in this repo.
- In citation lists on the site, the owner's own entry follows the author
  form stored in the vault (`Yeffal A`), as for all other authors (0004).

## Alternatives

- Full name with all given names and both surnames: rejected, because it
  does not match the name on the papers and would split search results.
- Initials only: rejected, because it is less findable.

## Consequences

- The name is plain text on the site, so it can change later without
  breaking any URL. Item IDs contain only the first author's surname (0003).
- If the owner later adopts a longer or different form, older papers will
  still be listed under the published form, and a note on the home page may
  be needed to link them.
