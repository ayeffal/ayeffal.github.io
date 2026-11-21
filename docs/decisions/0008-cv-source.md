# 0008. CV: same item list as the site, two contact variants

Status: accepted, 2026-11-21

## Context

CLAUDE.md says registry notes feed both the site and the PDF CV. The CV tool
lives in the separate vault repo. The owner will not list work "in
preparation" or "submitted" on any CV, because of the risk that ideas get
taken. The owner will list items that are published, in press, or on a
preprint server. Institutional requirement points and file or resolution
numbers do not belong on a CV.

## Decision

- For papers, talks and posters, site and CV use **the same allowlist and the
  same eligible statuses** (published, in press, preprint; see 0002). The CV
  tool may add item types the site does not show (degrees, positions,
  teaching, courses). Those are the CV tool's business and are not specified
  here.
- Two CV variants differ only in the **contact block**:
  1. **Public CV**, may be hosted on the site at a stable URL, overwritten
     when updated, with its date shown. Contact is the "(at)" email shown on
     the site (below) and ORCID. No phone or address.
  2. **Individual CV**, sent to specific people or institutions. It may add
     phone, a direct email and perhaps an address. It is never in this repo
     and never on the site.
- Contact details for the individual CV come from a local file kept outside
  this public repo, not from the registry notes.
- DNI/CUIL appear in neither variant by default.
- The vault repo builds the CV and also **writes one site export file**,
  holding only eligible, consent-marked items and only allowlisted fields. This
  repo's `sync` reads only that export, never the vault, so only the vault
  repo knows the vault's layout. This holds for now and may be revisited.
  - Agreed 2026-11-21: schema version 1, at `shared/cv/out/site-export.yaml`
    in the vault. Consent is a vault field set only by the owner. Records are
    keyed by a stable `uid`. The export is built in a separate private
    vault-side repository, so site and CV share one eligibility rule. Format:
    `design/reply-from-vault-agent.md`. Sample: `design/site-export.sample.yaml`.
    `sync` fails on any other `schema_version`.
- Site contact format: an institutional email written with " (at) " and
  " (dot) " in place of the symbols, no `mailto:` link. The address, written only in
  the obfuscated form, is `ayeffal (at) unsam (dot) edu (dot) ar`. The
  plain form must never appear in a tracked file, or the format is useless.

## Alternatives

- A wider CV allowlist: dropped, because the owner will not list in-review or
  in-preparation work, and requirement points are not CV content.
- A contact form: rejected, because forms are a non-goal, they need a
  third-party service, and they still get spam.
- One CV with contact details for everyone: rejected, because the owner wants
  phone and email only for chosen recipients.

## Consequences

- For papers, talks and posters there is one list, so no two-list drift to
  check.
- The individual CV needs a place to store contact details and a build option
  for each variant.
- Anything on the public CV stays findable even after it is replaced.
- The "(at)" format reduces simple scraping but does not stop modern scrapers.
