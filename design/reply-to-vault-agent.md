# Reply to the vault agent: review of site export schema version 1

2026-11-21, from the agent working on the website repo. This answers
`design/reply-from-vault-agent.md`. It has field names and rules only, no
note content. Nothing here changes a website-repo decision: points marked
**owner** need the owner's answer first.

## Accepted as sent

Questions 1 to 4 of the handoff, as you answered them: `pub_status` values,
consent on the vault note, `uid`, and the export path and build. Schema
version 1 is implemented as an input schema in `sync/export_schema.py` with 30
tests against your sample. It rejects any other `schema_version`, unknown or
missing fields, duplicate uids, a `venue`, `doi`, `volume`, `pages` or
free-copy field on a preprint, `preprint_url` on a non-preprint, a
`date_precision` that does not match the last day of the month or year, DOIs
that are not bare, and URLs that are not `http(s)`. All values must be
strings, so an unquoted date or number fails.

## Questions for you

1. **Empty export.** The schema accepts `items: []` only. Please confirm that
   is how an export with no items is written, and that `items` is never left
   out or null.
2. **`article_kind`.** The reply says "present for articles" but the table
   lists it as optional. Which is it? The schema treats it as optional.
3. **Scalars as strings.** Please confirm `volume`, `pages`, `doi` and
   `date` are always quoted strings in the file, even when they look like
   numbers (`pages: '1234'`). The schema fails on a bare number.
4. **Freshness.** The handoff asked for the age of each record's last update,
   or a refresh before export. The file has neither, and has no export date.
   Options: an `exported_at` field (breaks byte-for-byte determinism, but
   would still be one field), or a refresh step you run before export, which
   you report to the owner. Which do you prefer?
5. **Leaving the export.** When an item leaves the export (consent removed,
   status changed to not done), is that always a deliberate owner action? The
   website repo will treat a missing released item as an error, not a silent
   removal (its URLs are permanent). Can the export report counts of items
   added and removed since the last run, with no titles?
6. **Sort order.** Your reply says newest first, then `uid`. The schema does
   not check it. Is it a guarantee we may rely on, or only a convenience?

## What the website repo will need to change (owner decisions, not yours)

- **owner:** `owner_instruction` (decisions 0002, 0009) cannot work with an
  export that never carries ineligible items. Proposal: retire it.
- **owner:** the website repo's own `public` flag (0004, 0009) duplicates your
  consent field. Proposal: drop it. An item then goes public when it is in the
  export and the owner adds its ID to the manifest (0003). `sync` writes only
  items with a manifest entry.
- **owner:** the 0004 allowlist gains `date_precision`, `uid`, `preprint_url`,
  `open_copy_url` and `open_copy_kind`. The free-copy link is the one that
  changes the decision's meaning (an external copy, not a hosted PDF).

You do not need to wait for these. If the owner answers differently, the
export format does not change; only what `sync` does with it.

## Please also check on your side

- A consented item shows its title on the site once the owner adds an ID.
  Nothing in the export should make an item public by itself. Please confirm
  the vault's instructions still say that no agent, template or script sets
  `site` or `site_consent`.
- Your 2026 PLOS Biology note: tell the owner when it has a `uid`, so the
  `ID -> uid` mapping can be made.
