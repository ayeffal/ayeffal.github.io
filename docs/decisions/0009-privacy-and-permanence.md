# 0009. Privacy enforcement, owner instruction, mistakes and permanence

Status: accepted, 2026-11-21

## Context

The Goldfish review of decisions 0001 to 0007 found that privacy rested on one
local rule, that the unpublished-work rule had no defined mechanism, and that
permanence and takedown were unenforced. Git history keeps everything that was
ever committed.

## Decision

**Visibility (changed 2026-11-21).**
- Consent is a vault field set only by the owner (`site: public` and
  `site_consent`). The vault's export carries only consent-marked, eligible
  items (0008). An agent never sets consent.
- An item appears on the site only when it is in the export and has an entry
  in the manifest. `sync` writes only items with a manifest entry and reports
  the rest as counts. Adding the entry is the owner's act (0003).
- There is no override for unpublished work: the `owner_instruction` field is
  retired, because the export never carries ineligible items.
- A released item missing from the export is an error in `sync`, never a
  silent removal. A withdrawn item becomes a tombstone (below).

**Mistakes.**
- A history rewrite is allowed only for a privacy leak (a title, ID number,
  path or an unpublished manuscript), and only with the owner's approval each
  time.
- Anything that was ever pushed is treated as exposed anyway. GitHub keeps
  cached copies, forks and old pull-request references. Removing sensitive
  data for sure needs a request to GitHub support.

**Technical defaults.**
- Two programs: a local `sync` that reads the vault export (0008), and an
  automatic `build` that reads only committed files. The rule to fail on a
  missing field belongs to `sync`. `sync` writes its output atomically and
  prints a report without values or titles. It has a dry-run mode.
- The allowlist is a machine-readable schema that rejects extra keys. A scan
  looks for absolute paths, usernames and DNI/CUIL.
- Both checks run as a pre-commit hook and again in the automatic build,
  before deploy. The data carries a `schema_version`.
- A committed ledger of released URLs, checked by the build, so a published
  URL cannot vanish. The manifest is append-only. A withdrawn item becomes a
  tombstone page.
- Paper pages carry citation meta tags. The site links the owner's ORCID and
  has a sitemap.
- A hosted file is capped at 5 MB.

## Alternatives

- Rely on the hookify rule alone: rejected, because it runs only on one machine
  and can be skipped.
- Never rewrite history: rejected, because a leaked unpublished title is worth
  a rewrite in some cases.

## Consequences

- More machinery before the first commit of data, in line with CLAUDE.md's
  pending setup item.
- The ledger and manifest add one more file to keep consistent.
- None of this is built yet.
