# Academic website

*   **Author:** Abraham Yeffal
*   **Status:** Approved 2026-11-25. Review amendments of 2026-11-26,
    2026-11-27 and 2026-11-28 were approved by the owner during the EGM
    review (`design/zoom_out_report.md`, `design/comprehension_report.md`,
    `design/goldfish_review_report.md`).
*   **Date:** 2026-11-24
*   **Dates in parentheses** such as "(2026-11-26)" mark choices made in
    this design. They go into the decisions listed under "Decision updates
    this plan needs" (Technical Plan).

--------------------------------------------------------------------------------

## Overview

A personal academic website at `https://ayeffal.github.io/`, hosted on GitHub
Pages, for a PhD candidate in neuroscience in Argentina. It has five pages:
Home, Research, Papers, Talks and posters, and CV (0010).

The data comes from a private notes vault. A program in a separate private
vault-side repository writes one export file holding only papers, talks and
posters that the owner has marked public there, and only allowlisted fields
(0008). In this repo, a local script, `sync`, reads that file and writes
committed data files. The `build` job in GitHub Actions turns the
committed files into pages with Quarto and deploys them (0006, 0009). The
build never sees the vault or the export.

A paper, talk or poster gets its own permanent page at `/<type>/<id>/` only
when it has a summary written by the owner, a hosted file, or (for a CC BY
paper) its real abstract. Otherwise it is a row on its list page that links
to the publisher or to a public page (0002). The CV page shows the public CV
PDF once the vault side builds it; until then it is a placeholder (0008).
The site is English-only, with `/es/` reserved (0001).

Decisions 0001 to 0010 in `docs/decisions/` are the source for this design.
Where `design/concepts_brief.md` disagrees with them, the decisions win (see
"Superseded lines in the brief" below). The fields of an export record
(`type`, `format`, `date_precision`, `pub_status`, `open_copy_kind` and the
rest) are listed in 0004 and shown in `design/site-export.sample.yaml`.

Terms used below:

*   **Vault agent**: the Claude Code session that works in the vault-side
    repository. Its written replies (`design/reply-*.md`) fixed the export
    format.
*   **Claude**: Claude Code, the AI coding assistant that writes this repo's
    code under the owner's review.
*   **hookify**: a Claude Code plugin whose rules block some of Claude's own
    commands. Its rules are local files, not tracked in git.
*   **`CLAUDE.local.md`**: an untracked notes file for machine-specific
    values, such as the vault's path.
*   **DNI, CUIL**: the Argentine national identity number and the
    tax/labour identification number.
*   **Manifest** (`data/manifest.yml`): the append-only list that gives each
    public item its permanent `type` and `id`, keyed by the export's `uid`.
*   **Pending file** (`sync-pending.yml`, gitignored): where `sync` lists
    new IDs and withdrawals for the owner to confirm (2026-11-28).
*   **Ledger** (`data/ledger.txt`): every page URL ever generated, including
    the fixed pages. A URL in it must keep working once pushed.
*   **Tombstone**: a page left at a withdrawn item's URL, saying it was
    withdrawn.
*   **Phase 2**: CC BY abstracts and hosted item files, built only when the
    first item needs them (see "Order of work").
*   **Step 0**: a throwaway Quarto test run before building (Detailed
    Implementation Plan).
*   **CI**: GitHub Actions. On each push to `main`, GitHub starts a fresh
    temporary machine, downloads the repo, installs the pinned Quarto and
    Python, runs the checks, builds the site and publishes it. If any check
    fails, nothing is published and the previous site stays up. Free for
    public repos.
*   **`build`**: the CI job that renders and deploys the site.
*   **Owner file**: a file only the owner writes. **Tool file**: a file only
    a program writes. No file is both (see "Who writes what").

## The Problem

The owner needs one public page that search committees, editors and
collaborators find when they look up the name "Abraham Yeffal", and that
joins the owner's papers, talks, ORCID, Google Scholar profile and
affiliations. No such page exists.

Three things make this harder than a plain personal page:

1.  **The records are private.** Papers, talks and posters are recorded in
    a private vault that also holds unpublished manuscripts, ID numbers,
    requirement points and personal notes. Copying from it by hand is slow
    and one mistake can publish something that git history then keeps
    forever.
2.  **The same records feed the PDF CV.** If the site and the CV are kept
    separately, they drift apart.
3.  **Links must not break.** GitHub Pages cannot do server-side
    redirects, and academics paste links to single items into CVs, forms
    and papers. A URL that moves or disappears breaks every saved copy.

The proposed solution: the vault side exports only what the owner has
approved; this repo copies only allowlisted fields from that export, checks
every commit and every build for private data, copies the public CV PDF only
after scanning it, and keeps a ledger so that no released URL can vanish.

## Goals

Each goal states how it will be checked.

*   **Findable.** Every paper page carries citation meta tags; the site has a
    sitemap listing every page; the home page links ORCID
    `0000-0002-9645-6664` and the one Google Scholar profile (0009, 0010).
    Check: the build fails if a paper page lacks the tags or a page is missing
    from the sitemap.
*   **Credible.** The home page shows the date of its last update; the
    affiliation lines are the ones fixed in 0010; the site and the public CV
    draw on the same vault records and eligibility rule (0008, 0010). After
    each `sync`, every item in the export is on the site (2026-11-27). Every
    paper, talk and poster on either CV is also in the export, so it is on
    the site after the next `sync`; the CV may list fewer items than the site
    (2026-11-28, `design/reply-4-from-vault-agent.md`). Check: `sync` stops
    if any exported item has no manifest entry; the build fails if the home
    page lacks the last-updated date.
*   **One source of truth.** Every paper, talk and poster shown on the site
    comes from the vault export. This repo adds only the owner's authored
    text (or a CC BY paper's abstract), the `id`, `related` links and `files`
    entries (0004). Check: `sync` is the only program that writes item data,
    and from the vault it reads nothing but the export and the public CV
    PDF.
*   **Private by construction.** The local hooks refuse a commit or a push,
    and CI refuses a deploy, if the committed data holds a key not on the
    allowlist, an absolute path, a DNI/CUIL pattern, the plain form of the
    contact email, a phone number or an address. The username check runs
    only in the local hooks. The hooks can be skipped on purpose (see "Risks
    and Mitigations"). The public CV PDF's text gets the same scan before
    `sync` writes it (0008). The checks run before each commit, before each
    push and again in `build` (0009). Committed PDFs and images (the CV,
    hosted files, the headshot) have their metadata stripped (0004, 0008,
    0010). Check: a test commit with each kind of leak, including a file with
    metadata, is refused by the pre-commit hook; the same commit made with
    `--no-verify` is refused by the pre-push hook.
*   **Permanent URLs.** Every page URL that has been pushed (an item page,
    a list page, the home, research or CV page) keeps reaching its page or
    a tombstone. GitHub Pages cannot do server-side redirects, so URLs are
    chosen to never need changing, and an ID is never reused for a
    different item (0002). Pages do not move (2026-11-26). Hosted files are
    not in the ledger: a file can be taken down (see "Co-author removal
    request"). Check: the build fails if any URL in the ledger has neither
    a page nor a tombstone.
*   **Zero cost, no lock-in.** The site builds from a fresh clone with
    Quarto 1.11.9 (pinned, not yet tested) and Python, and uses no paid
    service (0006). Check: a CI build from a clean checkout succeeds.
*   **Adding an item takes under 10 minutes.** Measured from "the item is in
    the export" to "the change is pushed". Check: a timed walkthrough with the
    first real item. Not yet shown.

## Non-Goals

*   Blog, analytics, trackers, comments, forms (including a contact form),
    custom domain (CLAUDE.md, 0008).
*   Spanish pages. `/es/` is reserved only (0001).
*   Item pages for courses, awards, software or datasets; teaching and news
    pages (0002, 0010).
*   Any unpublished manuscript (submitted, in review, in preparation, draft),
    as a page or a row, unless it has a preprint, and then only as that
    preprint. There is no override (0002, 0009).
*   Building the export or the CV. Both belong to the vault-side repository
    (0008). This design only reads the export and hosts the public CV PDF.
*   Hosting files over 5 MB on the site (0009). They are external links;
    Zenodo is chosen case by case (0004).
*   Showing or adapting a publisher abstract for a paper that is not CC BY
    (0007).
*   The individual CV and its contact details. They never enter this repo
    (0008).
*   Reading the vault from this repo, at any time (CLAUDE.md, 0008).

## Open Questions

None remaining.

## Settled Choices

Each is part of the Technical Plan; dates show when it was settled.

### Settled during drafting (2026-11-24, later amendments dated inline)

*   **Status spelling.** Data keeps the export's value `in-press`; pages show
    "In press".
*   **List order.** Lists sort by the item's current `date`, the export's own
    order (`date` descending, then `uid`). A preprint that is published moves
    to its publication date. Its ID and URL do not change.
*   **`author_position`** stays out of the site (0004, resolved).
*   **Withdrawal** uses a `withdrawn` date in the manifest (0009). An item
    with a page becomes a tombstone; an item with only a list row loses its
    row. The manifest entry stays, so the ID is never reused. `sync` adds the
    date after the owner confirms it in the pending file (2026-11-27,
    2026-11-28). Once pushed, a withdrawal is permanent: the item cannot
    return under the same `uid` or ID.
*   **IDs are suggested by `sync`** (changed 2026-11-27; was: typed by the
    owner into the manifest). The owner confirms each one in the pending
    file. The rule is under `data/manifest.yml` in "Data formats".
*   **Public CV PDF.** `sync` copies it from a fixed vault-side path, strips
    its metadata and scans its text before writing it (0008). Agreed path:
    `shared/cv/out/cv-public.pdf`. No CV builder exists yet, so a missing
    file means "no CV yet": `sync` skips it and the CV page is a placeholder.
*   **Search Console.** Register with Google Search Console and import into
    Bing Webmaster Tools, once the site is live (0010). Ownership is shown
    with the verification `<meta>` tag in the home shell, not an uploaded
    file.
*   **Pages do not move** (changed 2026-11-26, after the Stage 5 review). The
    earlier Quarto `aliases:` safety net (0002) had no input path: the
    manifest is append-only and generated pages are tool files. If the
    derived type disagrees with the manifest, the export is fixed. If a real
    move is ever needed, it is designed then; `aliases:` remains the likely
    tool. Tombstones stay for withdrawals.
*   **Co-author removal request.** A published author list is public record,
    so citations stay as published. The co-author's name is removed from the
    owner's own text and hosted files, and a hosted file they co-own is taken
    down: it is deleted and its `files` entry removed, and its URL stops
    working (only page URLs are permanent). If that leaves the page with no
    content, the owner writes a summary or withdraws the item.
*   **Larger files.** Files over the 5 MB cap (0009) are not hosted on the
    site. Zenodo (free, permanent, gives a DOI) stays an option the owner
    decides case by case; the item page then links to it.
*   **Summaries and abstracts (0007).** Abstracts are free to read but not
    free to reuse: they stay under publisher or author copyright unless the
    paper is CC BY. So the owner's summaries are written fresh in plain
    language, never reworded from the abstract. A paper published under
    CC BY may also show its real abstract, labelled with that license and
    its source, and that abstract alone gives the item a page (0002).
    CC BY status is checked against Crossref by DOI when the abstract is
    added; the license URL, DOI and check date are recorded in
    `data/abstract-licenses.yml`, and the build (offline) fails if they are
    missing or not CC BY. A summary is optional: one never written is never
    an error and never blocks `sync`, the build or the item's list row.
    Removing the only content of a pushed page is an error (see
    "Lifecycle").
*   **Photo.** The home page shows a headshot (0010). The owner must hold its
    rights (own photo, or the photographer's written permission), and its
    metadata is stripped before commit.

### Superseded lines in the brief

`design/concepts_brief.md` predates the vault agent's replies. These lines
are out of date; the decisions named here are current. The brief itself is
unchanged.

*   Objection 4 proposes ZotLit's `zotero-key` as the record key. Current:
    the export's `uid` (0003). Registry notes are not managed by ZotLit.
*   "Consent kept only in the website repo: still open." Current: consent is
    a vault field set only by the owner (0009).
*   Open item 1 (vault agent). Answered: schema version 1, consent in the
    vault, records keyed by `uid` (0008).
*   Objection 2 "needs the vault agent's agreement". Given in both replies.

Reconciled at finalisation (2026-11-25, each decided by the owner):

*   "A page exists only when the item has a summary written by the owner or
    a hosted file." Current: a CC BY paper's real abstract also gives a page
    (0002, 2026-11-24).
*   "unpublished work excluded by default." Current: there is no override
    (0002, 0009).
*   "papers first would be the smallest start." Current: all three types
    and `related` are built at once; the first launch adds every item as a
    row first, then pages one item at a time ("Adding an item"). CC BY
    abstracts and hosted item files are Phase 2, built when the first item
    needs them (2026-11-26, see "Order of work").
*   "A program in the vault repo writes one export file." Current: a
    separate private vault-side repository (`vault-export`) writes it
    (reply 1, reply 3).

## Technical Plan (Architecture)

### Settled before drafting the Technical Plan (2026-11-25)

*   **Summaries are written on the website side**, never in the vault. Each
    text is written by the owner once (once more for a later Spanish
    version). Writing it in the vault was discarded: it would need export
    schema version 2, contradict 0004, and let private and public text sit
    side by side.
*   **Page layout: option A.** The owner writes `authored/<type>/<id>.md`.
    `sync` generates `<type>/<id>/index.qmd` from it and the committed data,
    and the generated page is committed. The repo therefore holds a
    generated copy of the text, which nobody edits. CI regenerates every
    page and fails if a committed page differs (see "Checks"). Rejected:
    owner-owned `index.qmd` with a Pandoc template (formatting in a template
    language the owner does not maintain, the reason Hugo was rejected in
    0006), and pages generated only in CI (the owner would never see the
    published pages in a diff, and errors would first appear in the GitHub
    log).

### Data flow

```text
 VAULT SIDE (private, read-only from here)
 ┌──────────────────────────────────────────────┐
 │ shared/cv/out/site-export.yaml   (schema v1) │
 │ shared/cv/out/cv-public.pdf      (optional)  │
 └───────────────┬──────────────────────────────┘
                 │ read by path in $VAULT_DIR (set in CLAUDE.local.md)
 OWNER'S COMPUTER▼
 ┌───────────────────────────────────────────────────────────────────┐
 │ sync = step 1 "import"  +  step 2 "generate"                      │
 │                                                                   │
 │ import:  export ──validate──► new uids: owner confirms an ID;     │
 │          missing uids: owner confirms withdrawal                  │
 │          (both in sync-pending.yml; sync stops until confirmed)   │
 │          ──► data/manifest.yml (append)                           │
 │          ──► data/items.yml                                       │
 │          cv-public.pdf ──strip metadata──► scan text              │
 │          ──► cv/cv-public.pdf + data/cv.yml   (only if changed)   │
 │                                                                   │
 │ generate (reads ONLY committed files, never the vault):           │
 │   data/items.yml + data/manifest.yml + authored/** +              │
 │   data/abstract-licenses.yml + data/cv.yml + data/ledger.txt      │
 │   ──► <type>/listing.yml, <type>/<id>/index.qmd, cv/index.qmd,    │
 │       data/ledger.txt (old entries + new URLs)                    │
 └───────────────┬───────────────────────────────────────────────────┘
                 │ git commit  ── pre-commit hook runs "checks"
                 │ git push
 CI (GitHub)     ▼
 ┌───────────────────────────────────────────────────────────────────┐
 │ checks ─► generate --check (regenerate, compare with commit)      │
 │ ─► quarto render ─► post-render checks ─► deploy to Pages         │
 │ any failure: stop, nothing deployed, old site stays               │
 └───────────────────────────────────────────────────────────────────┘
```

`generate` is one Python module used in two places: `sync` calls it to
write files, and CI calls it with `--check` to compare without writing.
Because it reads only committed files, CI can run it without the vault.
It never opens files itself: the caller passes a reader function
(`read(path) -> bytes | None`). The pre-commit hook reads the staged
version, the pre-push hook and CI read a commit, and `sync` reads the disk
with its import outputs laid over it. So each check compares the same
version of each file, and a file staged only in part is checked as staged.
This keeps the two programs of 0009: `sync` (local, the only reader of the
export) and `build` (CI: checks, `generate --check`, render, deploy).

### Repo layout

```text
_quarto.yml                 site config (hand-written once)
index.qmd                   home page shell; includes authored/home.md
research/index.qmd          research page shell; includes authored/research.md
papers/index.qmd            list page shell (Quarto listing of listing.yml)
papers/listing.yml          GENERATED: list rows
papers/<id>/index.qmd       GENERATED: item page or tombstone
papers/<id>/<file>.pdf      hosted file, Phase 2 (strip tool, run by owner; <= 5 MB)
talks/ ... posters/ ...     same shape as papers/
cv/index.qmd                GENERATED: CV page or placeholder
cv/cv-public.pdf            written by sync import (absent until a CV exists)
authored/home.md            OWNER: home text
authored/research.md        OWNER: research text
authored/<type>/<id>.md     OWNER: an item's summary, related, files, abstract
images/headshot.jpg         written by the strip tool, run by the owner
data/manifest.yml           written by sync import after the owner confirms: one entry per public item (append-only)
sync-pending.yml            GITIGNORED: written by sync import, confirmed by the owner, deleted by sync
data/items.yml              written by sync import: export records kept
data/cv.yml                 written by sync import: date of the current CV
data/abstract-licenses.yml  written by the abstract-license tool only
data/ledger.txt             written by generate: every page URL ever generated, fixed pages included
sync/                       export_schema.py (exists), sync, generate,
                            abstract-license tool, metadata-strip tool, tests
checks/                     pre-commit and CI checks, post-render checks, tests
.githooks/pre-commit        runs checks on the staged files
.githooks/pre-push          runs checks on every commit being pushed
.github/workflows/build.yml CI: checks, generate --check, render, deploy
requirements.txt            pinned Python packages
LICENSE, LICENSE-CONTENT.md MIT for code; CC BY 4.0 notice for content (0007)
```

Quarto renders only an explicit list of `.qmd` files (`render:` in
`_quarto.yml`: the home, research and CV shells and the `.qmd` files under
`papers/`, `talks/` and `posters/`), so the `.md` files in `authored/`,
`design/` and `docs/` never become pages. A post-render check makes sure
of it (below). Every page lives at `<dir>/index.qmd`, so it builds to
`<dir>/index.html` and is reached at `<dir>/`, as 0002 requires.

### Who writes what

| File | Written by | Never written by |
| :--- | :--- | :--- |
| `authored/**` | owner | any program; Claude |
| `data/manifest.yml` | `sync` import, only after the owner confirms in `sync-pending.yml` | owner by hand, Claude |
| `sync-pending.yml` (gitignored) | `sync` import writes it; the owner edits only `id` and `confirm` | Claude |
| `data/items.yml`, `data/cv.yml`, `cv/cv-public.pdf` | `sync` import | owner, Claude |
| generated pages, `listing.yml`, `data/ledger.txt` | `generate` | owner, Claude |
| `data/abstract-licenses.yml` | abstract-license tool | owner, Claude |
| hosted files, headshot | metadata-strip tool, run by the owner on a copy in `staging/` (gitignored). The owner may delete them, never edit them. | `sync`, Claude |
| shells, `_quarto.yml`, code, workflow | Claude, reviewed by owner | `sync` |

Guards:

*   Each program has a fixed list of paths it may write and refuses any
    other path. The owner's files are on no list.
*   Every generated file starts with a comment saying it is generated and
    naming its source. A hand edit is caught by `generate --check` in the
    pre-commit hook and in CI.
*   `.claude/settings.json` (tracked) denies Claude's Edit and Write tools on
    `authored/**`, `data/manifest.yml` and `sync-pending.yml`. A deny rule
    does not cover shell commands, so the hookify rule (Pending setup in
    CLAUDE.md) also blocks shell writes to those paths. Claude proposes text
    changes in chat and the owner makes them.
*   `sync` never prompts (2026-11-28). New IDs and withdrawals wait in
    `sync-pending.yml` until the owner confirms them there, so `sync` runs
    the same from any shell, and a run Claude starts stops at the pending
    file. This stops accidents; it is not a security control. The control
    is that every new manifest entry shows in the commit diff the owner
    reviews.
*   **Change to 0004 (proposed here):** the CC BY license record (`url`,
    `doi`, `checked` date) moves out of the owner's authored file into
    `data/abstract-licenses.yml`, keyed by `<type>/<id>`. That way no program
    ever writes into a file the owner wrote. The abstract text itself stays
    in the owner's file.

### Data formats

**`data/manifest.yml`** (`sync` import after the owner confirms,
append-only). A list of entries:

```yaml
- uid: "r-p7m2kw4d"        # export key, ^r-[a-z0-9]{8}$
  type: "papers"           # papers | talks | posters
  id: "surname-2026-tag"   # 0003 format
  withdrawn: "2027-01-15"  # optional; the only field ever added later
```

Rules, checked by `checks`: `uid` unique; `(type, id)` unique; `id` matches
`^[a-z]+(-[a-z]+)*-\d{4}-[a-z]+(-[a-z]+)?$`; compared with the previous
commit, no entry is removed or reordered and no field changes except that
`withdrawn` may be added.

**ID suggestion** (2026-11-27, cases added 2026-11-28). For each exported
item with no manifest entry, `sync` proposes an ID in the 0003 format:

*   **Surname**: the first author's surname, lowercased, accents removed,
    other non-letters dropped; spaces between parts become hyphens
    (`de la Fuente` → `de-la-fuente`).
*   **Year**: the year of the record's `date` when the ID is made. It does
    not change if the date changes later (0003).
*   **Tag**: the first title word that, reduced to ASCII letters, has 3 or
    more letters and is not a short common word ("the", "and", "for" and
    so on). `2D` becomes `d` and is skipped. If `(type, id)` is taken, the
    next such word is added. If that is taken too, `id` is left empty for
    the owner to fill in.

Every `id`, suggested or typed, is checked against the regex above and
for uniqueness. Once written, the ID is fixed for good (0003). The consent
check stays in the vault (`site: public` and `site_consent`, 0009): being
in the export means being shown.

**`sync-pending.yml`** (2026-11-28; `sync` import writes it, the owner
confirms; gitignored). When the export has new or missing `uid`s, `sync`
writes this file, prints "N entries need your confirmation in
sync-pending.yml; nothing else was written" and exits 1:

```yaml
# PENDING: sync will not finish until every entry below is confirmed.
# New items: check the id (edit it if you like), then set  confirm: yes
# Missing items: set  confirm: withdraw  only to withdraw for good.
#   Once pushed, a withdrawal cannot be undone.
new:
  - uid: "r-p7m2kw4d"
    type: "papers"
    title: "..."
    id: "surname-2026-tag"   # suggested
    confirm: no
missing:
  - uid: "r-a1b2c3d4"
    id: "surname-2025-tag"
    title: "..."
    confirm: no
```

*   The next `sync` reads it. It finishes only when every `new` entry has
    `confirm: yes` and a valid, unique `id`, and every `missing` entry has
    `confirm: withdraw`; `yes` is refused for a withdrawal. It then writes
    the manifest and deletes the file. Otherwise it stops again and writes
    nothing.
*   Leaving `confirm: no` is how an entry is skipped for now. While any
    entry is unconfirmed, `sync` writes nothing.
*   If the export changed since the file was written, `sync` keeps the
    answers for entries that still apply, adds new entries unconfirmed,
    drops the rest and stops.
*   Before writing the file, `sync` stops with "export looks empty" if the
    export has no items while the manifest has entries not withdrawn.
*   The owner may change only `id` and `confirm`; any other change is an
    error.
*   The pre-commit hook refuses a commit while the file exists.
*   Titles appear here so the owner can recognise each item. The file is
    gitignored, and each title is already in the export or in the
    committed `data/items.yml`.

**`data/items.yml`** (sync import). The same shape as the export
(`schema_version: 1`, `items: [...]`), holding only records whose `uid` has
a manifest entry. The record of a withdrawn item is kept from the previous
`data/items.yml`, so its tombstone can still show the title. Order: `date`
descending, then `uid`, as in the export. It is validated with the existing
`sync/export_schema.py`, so the allowlist has one definition.

**`authored/<type>/<id>.md`** (owner). Front matter, all keys optional:

```yaml
related: ["talks/surname-2024-tag"]   # other items, as <type>/<id>
files:
  - url: "https://zenodo.org/..."     # external, e.g. a recording
    label: "Recording"
    rights: "© the authors"           # one-line rights note (0007)
  - path: "poster.pdf"                # Phase 2: hosted, in <type>/<id>/
    label: "Poster (PDF)"
    rights: "© the authors"
abstract: |                           # Phase 2, papers only: CC BY abstract,
  ...                                 # copied by the owner from the publisher
```

The body is the summary in the owner's words. Any other front matter key
is an error.

**Phase 2** means the parts built only when the first item needs them:
CC BY abstracts and hosted item files (see "Order of work"). Until then the
schema rejects `abstract` and `files[].path`, so neither can reach the site
unchecked.

**`data/abstract-licenses.yml`** (tool). `papers/<id>: {url, doi,
checked}`. Written by `sync/abstract-license` after it asks Crossref for the
item's DOI (taken from `data/items.yml`) and finds a license entry for the
published version (or with an unspecified version) whose URL starts with
`http(s)://creativecommons.org/licenses/by/` and whose `start` date is on
or before today, so an embargoed license does not count yet (2026-11-28).
The request sends a generic
User-Agent and no email. The tool refuses to write anything for any other
license.

**`data/cv.yml`** (sync import). `date: "YYYY-MM-DD"`, the day `sync` last
wrote a changed CV PDF. Absent until a CV exists.

**`data/ledger.txt`** (generate). One page path per line, for example
`/papers/surname-2026-tag/`. `generate` writes the old lines plus every
page it now produces, including the fixed pages (`/`, `/research/`, the
three list pages, `/cv/`), sorted. A line is never removed. A URL becomes
permanent when the commit that adds it is pushed (see "Adding an item").
Hosted files and the CV PDF are not listed: their URLs are kept stable by habit, not by a
check, so a file can be taken down.

**`<type>/listing.yml`** (generate). Quarto listing contents. Every value is
a display string worked out in Python: `title`, `citation` (authors, venue,
volume, pages), `date_display` (day, month or year per `date_precision`),
`status_display` (`In press`, `Preprint`, empty if published), `path` (the
item page if it has one, otherwise `https://doi.org/<doi>`, the preprint URL
or `url`) and `page` (a text marker when a page exists; an icon is
untested, 0006). Quarto only lays the rows out, with sorting off so the file
order is kept.

### What `generate` decides

*   **Type**: `publication` → `papers`; `communication` with `format: poster`
    → `posters`; `oral` or `lecture` → `talks`. If this disagrees with the
    manifest's `type`, it is an error, fixed in the export (pages do not
    move).
*   **Page or row**: an item gets a page when its authored file has a
    non-empty body, at least one `files` entry, or (papers) an `abstract`.
    Otherwise it is a row only.
*   **Item page content**: title; citation line; status; links (DOI, free
    copy with its kind, preprint, public `url`); summary; CC BY abstract
    labelled "Abstract: CC BY, from doi:<doi>" with the license link; files,
    each with its rights note; related items (each linked to its page or,
    for a row-only item, to its external link; withdrawn items left out).
*   **Citation meta tags** (paper pages only, not tombstones), written into
    the page's `include-in-header`: `citation_title`, one `citation_author`
    per author as `Surname, Initials`, `citation_publication_date` (`YYYY/MM/DD`,
    `YYYY/MM` or `YYYY` per precision), and when present
    `citation_journal_title`, `citation_volume`, `citation_firstpage`,
    `citation_doi`. Written by `generate`, not by Quarto's `google-scholar`
    option, because Quarto would parse `Yeffal A` as a personal name
    (untested) and add a citation box that is not wanted.
*   **Tombstone**: an item marked `withdrawn` whose page URL is in the ledger
    gets a page with its title, the date of withdrawal and a one-line notice.
    It has no summary, no files and no meta tags. A withdrawn item without a
    page loses its row.
*   **CV page**: with `data/cv.yml`, a link to `/cv/cv-public.pdf` and its
    date; without it, a placeholder line.
*   **Output**: UTF-8, LF line endings, fixed key order, no timestamps, so the
    same inputs give the same bytes on Windows and on CI's Linux machine.

### Lifecycle

| Event | What happens |
| :--- | :--- |
| Owner marks an item public in the vault | Next `sync` writes a suggested ID to `sync-pending.yml` and stops. Once the owner sets `confirm: yes` and runs `sync` again, the entry is appended and the item gets a row (a page too if an authored file has content). |
| Preprint is published | Same `uid`, so the same ID and URL. The record updates in place, the row moves to the new date, and the summary stays. |
| Authored file gains content | The row gets a page; its URL enters the ledger. |
| Page loses all content (authored file emptied or deleted) | Error: the URL is in the ledger. The owner restores the content or withdraws the item. |
| Manifested item missing from the export, not withdrawn | `sync` lists it under `missing` in `sync-pending.yml` and stops. `confirm: withdraw`: the next `sync` adds `withdrawn: <today>`. Anything else: error (0009), nothing written. |
| Export has no items, but the manifest has entries not withdrawn | Error "export looks empty", before any pending file is written. Nothing written. |
| Item marked `withdrawn` but still in the export | Error (0009). |
| Item withdrawn | Tombstone if it had a page; otherwise the row goes. The manifest entry stays. Its hosted files are deleted by the owner. |
| Hosted file taken down (Phase 2) | The owner deletes the file and its `files` entry. Its URL stops working. If the page has no content left, it is the "page loses all content" error above. |
| `related` names an item not in the manifest | Error. |
| Export `schema_version` is not 1 | Error, nothing written (0003). |
| CV PDF appears or changes | Stripped, scanned, written with a new `data/cv.yml` date. A failed scan stops `sync`. |
| CV PDF unchanged apart from metadata | Nothing written. "Unchanged" means the stripped PDF has the same bytes as the committed one. If stripping doesn't give the same bytes every run, it means instead that the vault PDF's SHA-256 matches the one in `data/cv.yml`. A throwaway test before building (Step 0 #10) settles which. |

`sync` computes every output and runs every check in memory before writing
anything, then writes each file through a temporary file and a rename. Its
report gives counts only (`N rows, N pages, N tombstones, N new IDs, N
withdrawn`), never titles or values (0009). Titles appear only in
`sync-pending.yml`, which is gitignored and never printed. The pending
file is settled first, so every check still runs on the full result
before anything is written. `--dry-run` writes nothing, not even the
pending file, and prints the report (with "N items need an ID" and "N
missing from the export" if any).

`sync` refuses to run if `git config core.hooksPath` is not `.githooks`,
so the pre-commit hook cannot be silently inactive.

### Checks

**`checks`** run in the pre-commit hook (on the staged version of each
file), in the pre-push hook (on every commit being pushed) and again in CI
(on the pushed commit):

1.  **Allowlist.** `data/items.yml` passes `sync/export_schema.py`;
    `data/manifest.yml`, `data/cv.yml`, `data/abstract-licenses.yml` and the
    authored front matter pass their own schemas, which reject unknown keys.
2.  **Privacy scan** of every text file that can carry vault data or is
    published: `data/`, `authored/`, the generated pages and listings, the
    shells (`*.qmd`, `_quarto.yml`, `_includes/`), `README.md` and
    `LICENSE*`. The scope is one list next to the patterns. Code, tests,
    `design/`, `docs/` and `.github/` are not scanned: they contain the
    patterns themselves and never receive vault data (CLAUDE.md's privacy
    rules cover them). The scan looks for absolute paths, DNI and CUIL
    patterns, any email address in plain form, phone numbers, street-address
    words and Argentine postal codes. The username check runs only in the
    local hooks, using the machine's current username and home path,
    because the username is in no tracked file and CI cannot know it.

    The patterns are pinned to avoid normal publication data (2026-11-28):
    phone numbers need a `+54` prefix, or 8 or more digits in groups split
    by spaces or dashes, and are not looked for in a `pages` field. Postal
    codes are matched only in the CPA form (a letter, four digits, three
    letters); the old four-digit form cannot be told apart from a year and
    is not scanned. Known false positives (the ORCID iD, DOIs, `YYYY-MM-DD`
    dates) are exempt by pattern, in one list in the code. Every pattern is
    tested against the sample export and the generated pages, which must
    pass clean. Error messages name file and line, never the matched text.

    The absolute-path and username checks also run on `.claude/`,
    `CLAUDE.md`, `.githooks/`, `.github/`, `.gitignore`, `.gitattributes`
    and `requirements.txt` (2026-11-28). These files hold no vault data but
    are where machine paths creep in.
3.  **Binary files**: every committed PDF and image is at most 5 MB and has
    no metadata (PDF Info dictionary and XMP; image EXIF and XMP). Each PDF's
    text is extracted and gets the scan in 2. A poster that prints co-author
    emails is therefore refused until the emails are removed. Phase 2 hosted
    PDFs: the strip tool also drops annotations and embedded files, and a PDF
    with images but no extractable text is refused until the owner confirms
    it (2026-11-28). Image data inside a PDF is not re-encoded (see "Risks
    and Mitigations").
4.  **Abstracts** (Phase 2): every authored `abstract` has an entry in
    `data/abstract-licenses.yml` whose `doi` matches the item and whose URL
    is CC BY. No network call.
5.  **Append-only**: the manifest and the ledger, compared with `HEAD` in
    the pre-commit hook, with each commit's parent in the pre-push hook, and
    with the commit before the push in CI. If CI has no such commit (the
    first push or a manual run), or it is not an ancestor of the pushed
    commit (a force push after an approved rewrite), CI skips this check
    and says so in the log (2026-11-28). A leak is removed with
    `git filter-repo`, approved by the owner each time (0009). The
    rewritten commits never contained the entry, so the pre-push hook,
    which compares each commit with its parent, passes them.
6.  **`generate --check`**: regenerate in memory and compare with the
    committed generated files; any difference fails.
7.  **No pending file** (pre-commit hook only, 2026-11-28): the commit is
    refused while `sync-pending.yml` exists, so half-confirmed work is not
    committed.

**Post-render checks** (CI only, after `quarto render`):

*   Every ledger path exists in `_site` as a page or a tombstone.
*   Every non-tombstone paper page has `citation_title`, `citation_author`
    and `citation_publication_date`.
*   `sitemap.xml` lists every built page except tombstones; `/x/index.html`
    and `/x/` count as the same URL.
*   The home page shows "Last updated YYYY-MM-DD". CI passes the date of the
    last commit that touched `data/`, `authored/` or a shell
    (`git log -1 --format=%cs -- data authored '*.qmd'`) to Quarto as
    metadata (`-M`), so a code-only commit does not move it (2026-11-28);
    the home shell prints it.
*   `_site` holds nothing from `design/`, `docs/`, `data/`, `authored/`,
    `sync/` or `checks/`.
*   No third-party requests: no built HTML or CSS loads a script, style or
    font from another site. Links are allowed. This is why the site uses
    Quarto's default Bootstrap theme: some Bootswatch themes import Google
    Fonts.

What the hooks cannot do is under "Risks and Mitigations".

### Site configuration

*   `_quarto.yml`: website project, `site-url: https://ayeffal.github.io/`,
    `output-dir: _site`, the explicit `render:` list, default theme, search
    off (five pages need none), navbar with Home, Research, Papers, a "Talks
    and posters" menu (Talks, Posters) and CV.
*   Footer: the contact line `ayeffal (at) unsam (dot) edu (dot) ar` (no
    `mailto:`), "Content CC BY 4.0" and "Code MIT", each linked (0007, 0008).
*   Home shell: headshot, name (0005), the two affiliation lines (0010), the
    included home text, ORCID and Scholar links, last-updated date. Its
    header carries a JSON-LD `Person` block: name, ORCID and Scholar as
    `sameAs`, affiliations in English with the Spanish official names as
    `alternateName` (0010).
*   Research shell: the included research text and the "in Spanish" line
    with the Spanish official names (0010).

### CI workflow

On push to `main` (or a manual run): check out with full history (needed
for the append-only check), set up Python 3.13 and install the pinned
`requirements.txt` (PyYAML, pypdf, Pillow), run `checks` and
`generate --check`, install Quarto 1.11.9 with `quarto-dev/quarto-actions`,
render with the last content-commit date, run the post-render checks,
then upload `_site` and deploy with GitHub's Pages actions. One-time
manual step: set the repo's Pages source to "GitHub Actions".

### Adding an item (target: under 10 minutes)

1.  In the vault: mark the item public; run the vault-side export.
2.  Run `sync`. It stops and writes the new item's title and a suggested ID
    to `sync-pending.yml`.
3.  Open `sync-pending.yml`, check or change the `id`, set `confirm: yes`,
    and run `sync` again. The item gets a row and the pending file is
    deleted.
4.  Optional: write `authored/<type>/<id>.md`. For a CC BY abstract
    (Phase 2), paste it and run the abstract-license tool.
5.  Optional (Phase 2): put a file in `staging/`, run the metadata-strip
    tool into `<type>/<id>/`, and list it under `files`.
6.  If you did step 4 or 5, run `sync` again so the item gets its page.
    Preview locally with `quarto preview` if wanted.
7.  Commit (the pre-commit hook runs the checks) and push (the pre-push
    hook checks again; CI deploys).

A page URL becomes permanent once its commit is pushed: this is the one
definition of "pushed" used in this design. Before the push, the commit
can still be dropped.

### Withdrawing an item

Withdrawal starts in the vault: `sync` only offers to withdraw an item
that has left the export (0009).

1.  In the vault: remove the item's consent; run the vault-side export.
2.  Phase 2: delete its hosted files and their `files` entries.
3.  Run `sync`. It stops and lists the item under `missing` in
    `sync-pending.yml`. Set `confirm: withdraw` (the word in full; `yes` is
    refused) and run `sync` again. It adds `withdrawn: "<today>"` to the
    manifest entry. A page becomes a tombstone; a row-only item loses its
    row.
4.  Commit and push. From then on the withdrawal is permanent.

For a co-author's request to remove a hosted file, only step 2 applies,
then steps 3 (a plain `sync` run, with no pending file) and 4 (see
"Co-author removal request").

**Suggested order for the first launch (decided 2026-11-25).** Add every
public item as a row first (steps 1, 2 and 6 only), so the site launches
with complete lists. Then give items pages one at a time, adding a
summary, CC BY abstract or hosted file per item. Hosted files and rights
notes, the part most likely to leak co-author data, then come after the
pipeline has run on real data. This is the owner's habit, not a rule the
code enforces.

### Decision updates this plan needs

Applied only after the design is approved:

*   **0002** (added 2026-11-26): the `aliases:` safety net is withdrawn;
    pages do not move; the ledger holds page URLs only, so a hosted file can
    be taken down.
*   **0003** (2026-11-27, 2026-11-28): `sync` suggests each ID and the
    owner confirms or retypes the tag in `sync-pending.yml`; the year is
    the year of the record's `date` when the ID is made; the manifest is
    written by `sync`, never by hand.
*   **0004**: the license record moves to `data/abstract-licenses.yml`
    (above); `related` and `files` live in the authored file's front matter.
    The visibility rule is the vault consent plus the owner's confirmation
    of the ID in `sync-pending.yml` (2026-11-27).
*   **0007**: the CC BY license record is in `data/abstract-licenses.yml`,
    not in the authored file; a license counts only from its `start` date
    (2026-11-28).
*   **0006**: generation is a separate step that reads only committed files;
    CI reruns it and compares. Pages are still committed. The "CV advantage
    of one toolchain" lapsed with 0008 (the CV is built on the vault side);
    Quarto stays for maintainability from Python and R and for the navbar,
    theme, listings and sitemap (2026-11-26).
*   **0009**: `build` also runs `generate --check`; the local hooks, not CI,
    are the privacy gate for what reaches GitHub; a pre-push hook re-checks
    every pushed commit (2026-11-26); `sync` refuses to run without the
    hooks. `sync` does not finish while an exported item has no ID, which
    replaces "reports the rest as counts"; a withdrawal is confirmed by the
    owner in `sync-pending.yml` with the word `withdraw`, and `sync` adds
    the `withdrawn` date (2026-11-27, 2026-11-28). CI skips the append-only
    check when the commit before the push is missing or not an ancestor, so
    an approved history rewrite can deploy (2026-11-28).

## Risks and Mitigations

Each line is risk → mitigation.

**What the hooks cannot do.** The repo is public. Once a commit is pushed,
GitHub shows it, whatever CI decides; CI can stop the deploy, not the
exposure. The local hooks are therefore the privacy gate, and CI is the
backstop for the deploy. GitHub offers no server-side hook that could
refuse a push on github.com. Rejected for now (2026-11-26): a private
source repo whose CI pushes only the built site to the public repo. It
closes this gap but adds a second repo and a deploy secret, which one
owner committing from one machine does not need.

*   **Hooks skipped.** The pre-commit hook can be skipped with
    `--no-verify` → the pre-push hook re-checks every commit in the push.
    Both can be skipped on purpose → the hookify rule blocks Claude from
    doing it; for the owner it is a deliberate act.
*   **Hooks not enabled in a clone.** Neither hook runs where
    `core.hooksPath` is not `.githooks` → `sync` refuses to run without it;
    a commit made without `sync` (a typo fix in `authored/`) still relies
    on it being set once per clone (README setup step).
*   **Mistaken withdrawal.** A broken or partial export could list items as
    missing, and a pushed withdrawal cannot be undone → `confirm: no` is
    the default, a withdrawal needs the word `withdraw`, and an empty export
    stops `sync` before anything is offered.
*   **Something else confirms on the owner's behalf.** Claude or a script
    could edit `sync-pending.yml` → Claude's tools are denied on it and the
    hookify rule blocks shell writes; every new manifest entry still shows
    in the commit diff the owner reviews.
*   **Scans catch formats, not meaning.** A summary that names an
    unpublished study passes every check → the owner reads every diff
    before committing.
*   **Old four-digit postal codes are not scanned** (they look like years)
    → addresses never enter the export, and the owner reads the diff.
*   **Commit metadata is public.** Author and committer emails appear on
    GitHub → this clone commits with the GitHub noreply address; keep it
    that way.
*   **Image data inside a PDF is not re-encoded** (Phase 2 hosted files) →
    accepted for now; image-only PDFs need the owner's confirmation, and
    the owner reads each file before hosting it.
*   **Quarto 1.11.9 behaviour is untested**: `render:` globs that skip
    `.md`, listings with external `path` values and `sort: false` (one
    external link was tested, 0006), `-M` metadata on a website render, the
    sitemap's URL form → Step 0 tests each one with a fallback; if several
    fail, Alternative D's Python renderer is reconsidered.
*   **Byte-identical output on Windows and Linux** is assumed, not tested
    → `.gitattributes` forces LF; `generate --check` in CI fails on any
    difference, so a mismatch is caught, not shipped.
*   **CV stripping may not be repeatable** (pypdf may write a new `/ID`)
    → Step 0 #10; the fallback is the hash rule in the Lifecycle table.
*   **Google Scholar may ignore, or wrongly merge, a page** that carries
    citation tags but not the full text → only the tags are under our
    control; after launch, check each paper with Scholar's own lookup.
*   **Scale.** PDFs build up in git history, which never forgets → 5 MB cap
    per file, and hosted files only in Phase 2, one item at a time. GitHub
    Pages limits a published site to 1 GB.

## Alternatives Considered

The architecture-level alternatives come first, each with pros, cons and
the reason it was rejected. Smaller choices already recorded in the
decisions follow in one table.

### Alternative A: Summaries written in the vault

A `site_summary` front-matter field on each vault note, exported only for
consent-marked notes under export schema version 2.

*   **Pros**: the text sits next to the record it describes; one place to
    look; the export's consent filter already limits it to public items.
*   **Cons**: needs schema version 2 and new work from the vault agent;
    contradicts 0004; the text still has to be copied into this repo,
    because the build cannot read the vault; private notes and public text
    sit side by side, and free text crosses the boundary without the owner
    reading it again, which no pattern scan can make safe; a typo fix takes
    four steps instead of two.
*   **Reason for Rejection**: Rejected (owner, 2026-11-25; recorded in
    `design/concepts_brief.md` and "Settled before drafting the Technical
    Plan"): public text is written where it is published, and the vault
    stays private notes only.

### Alternative B: Owner-owned `index.qmd` with a Pandoc template

The owner writes `<type>/<id>/index.qmd`; `sync` writes a `_metadata.yml`
beside it; a Quarto title-block template draws the citation and meta tags.

*   **Pros**: the owner's text appears once in the repo; no generated copy.
*   **Cons**: citation formatting lives in Pandoc template syntax, which the
    owner does not maintain; depends on Quarto's metadata merging and partials
    staying the same across versions (untested); a page with only a hosted
    file still needs a generated `index.qmd`, so ownership ends up mixed.
*   **Reason for Rejection**: Rejected (owner, 2026-11-25; "Settled before
    drafting the Technical Plan"): the same template-maintenance problem for
    which Hugo was rejected in
    [0006](../docs/decisions/0006-site-generator.md).

### Alternative C: Pages generated only in CI

Commit only data and authored text; CI generates the pages before
rendering, and they are never committed.

*   **Pros**: one step fewer when editing text (no `sync` rerun); a generated
    page cannot be edited by hand because none is in the repo; smallest
    diffs.
*   **Cons**: the owner never sees the published pages in a diff, only in a
    local preview; generation errors appear first in the GitHub log, a tool
    the owner does not use yet; reverses 0006's committed generated files.
*   **Reason for Rejection**: Rejected (owner, 2026-11-25; "Settled before
    drafting the Technical Plan"): what is committed should be what is
    published, and errors should appear in the
    terminal. The `generate --check` step in CI keeps the main benefit
    (no stale page reaches the site).

### Alternative D: Other site generators

Hugo, Jekyll, or HTML rendered directly by a Python script.

*   **Pros**: Hugo is one small program that makes the URLs by default.
    Jekyll is built by GitHub Pages itself. A Python script would need no
    site generator at all.
*   **Cons**: Hugo's Go templates and Jekyll's Ruby are outside what the owner
    can maintain; Jekyll's GitHub-built advantage is lost because the data is
    generated locally anyway. A Python renderer would mean writing the
    navbar, listings and sitemap by hand.
*   **Reason for Rejection**: Rejected
    ([0006](../docs/decisions/0006-site-generator.md)): Quarto is maintainable
    from Python and R, and gives the navbar, theme, listings and sitemap
    without hand-written HTML. 0006 also counted one toolchain for the site
    and the CV; that reason lapsed when 0008 moved the CV build to the vault
    side (noted 2026-11-26). Python now writes every page body, row, citation
    tag and tombstone, so Quarto's share is small. If several Step 0 items
    fail, a Python renderer is reconsidered instead of stacking fallbacks.

### Alternative E: Copy all vault fields, filter at render time

*   **Pros**: one copy step, no allowlist to keep in two places.
*   **Cons**: the repo's history would hold every private field once
    committed, and git cannot reliably forget.
*   **Reason for Rejection**: Rejected
    ([0004](../docs/decisions/0004-data-schema.md)): filtering happens on
    the vault side, before anything leaves it (0008), and again in `sync`.

### Alternative F: Privacy enforced only by the hookify rule

*   **Pros**: no extra code; already planned in CLAUDE.md.
*   **Cons**: it guards only Claude's actions on one machine; a commit made
    from a terminal or editor skips it.
*   **Reason for Rejection**: Rejected
    ([0009](../docs/decisions/0009-privacy-and-permanence.md)): the checks
    run as a git pre-commit hook and again in CI; hookify is an extra layer for
    Claude's shell commands.

### Alternative G: The `pre-commit` framework instead of a plain git hook

*   **Pros**: hooks install with one command and are versioned in a config
    file.
*   **Cons**: a new dependency for one hook that calls one Python script; it
    still needs a manual install per clone, the same as setting
    `core.hooksPath`.
*   **Reason for Rejection**: chosen while drafting the Technical Plan,
    approved with it on 2026-11-25: CLAUDE.md forbids unrequested
    dependencies, and `sync` refusing to run without the hook covers the
    "forgot to install" case.

### Alternative H: Quarto's `google-scholar: true` for citation meta tags

*   **Pros**: no code; Quarto writes the tags from front matter.
*   **Cons**: Quarto parses author names, and `Yeffal A` may be split into
    the wrong given and family names (untested); it also adds a citation box
    and BibTeX block to each page, which is not wanted.
*   **Reason for Rejection**: chosen while drafting the Technical Plan,
    approved with it on 2026-11-25: `generate` writes the tags itself, so
    the format is known and the post-render check can verify it.

### Alternative I: The owner types each manifest entry by hand

*   **Pros**: the owner picks every tag; no suggestion code.
*   **Cons**: copying each `uid` from the export file is slow and
    error-prone, and the site lags the export until it is done.
*   **Reason for Rejection**: Rejected (owner, 2026-11-27; Stage 6 finding
    C2, `design/comprehension_report.md`): `sync` suggests each ID and the
    owner confirms it.

### Alternative J: Confirm IDs and withdrawals at a terminal prompt

*   **Pros**: one `sync` run per change; no pending file to read and
    check.
*   **Cons**: the owner must type into a running command; native Windows
    Python under Git Bash (mintty) may not detect a terminal and refuse the
    owner's own run; the terminal check is easy to fake, so it guards
    nothing.
*   **Reason for Rejection**: Rejected (owner, 2026-11-28; Stage 7 finding
    K4, `design/goldfish_review_report.md`): the owner confirms in
    `sync-pending.yml` instead.

### Smaller choices already settled

| Alternative | Reason for rejection | Source |
| :--- | :--- | :--- |
| Bilingual from day one | Doubles writing and review for no current need. | 0001 |
| English under `/en/` | Longer links; moving English to the root later breaks them. | 0001 |
| Machine translation at build time | Sends text to an outside service; unreviewed output can misstate work. | 0001 |
| List pages with anchors only | Anchors are not permanent, citable addresses. | 0002 |
| Item pages for every type or item | Near-empty pages look worse than a row. | 0002 |
| Titles or dates in URLs | Titles change; preprint and published dates differ. | 0002 |
| `aliases:` instead of stable URLs | JavaScript-only redirects; clients without JavaScript see an empty page. (Since 2026-11-26 `aliases:` is not used at all.) | 0002 |
| Private source repo deploying to the public repo | Closes the `--no-verify` gap, but adds a second repo and a deploy secret; a pre-push hook is enough for one owner on one machine. | This plan (2026-11-26) |
| Unpublished work as "preprint soon" | Announces work before the owner and co-authors choose to. | 0002 |
| DOI, opaque or title-slug IDs; no year; type suffix; IDs unique across types | No DOI for talks; unreadable; titles change; tags collide; the path already gives the type. | 0003 |
| ZotLit `zotero-key` as record key | Registry notes are not ZotLit-managed; the vault's `uid` is used. | 0003 |
| Vault `pub_status` as the visibility switch | Cannot express "published but not approved for the site". | 0004 |
| Personal cloud links for files | Links break. Allowed only for large files. | 0004 |
| Publisher abstracts by default | Rights differ by publisher. Only CC BY abstracts, checked via Crossref. | 0004, 0007 |
| License record in the owner's authored file | A program would write into the owner's file. Moved to `data/abstract-licenses.yml`. | This plan |
| Full name or initials only | Does not match the papers; less findable. | 0005 |
| Apache-2.0, no code license, CC BY-NC-ND | Patent grant unneeded; blocks reuse; owner wants text shareable. | 0007 |
| Unpaywall, a hand-typed license field, Zotero Rights via ZotLit | Email in each request; mistakes uncaught; inconsistent and not ZotLit-managed. | 0007 |
| Wider CV allowlist; one CV with full contact for all | Owner will not list in-review work; phone and email only for chosen recipients. | 0008 |
| Contact form | Forms are a non-goal, need a third-party service, attract spam. | 0008 |
| Consent kept only in the website repo | Consent belongs with the record, set only by the owner in the vault. | 0009 |
| Never rewrite history | A leaked unpublished title can justify a rewrite, with approval each time. | 0009 |
| Single page; teaching, software, news, blog pages | Lists need their own URLs; no current content. | 0010 |
| Spanish-first affiliation, or Spanish in parentheses | English-first matches the papers and the supervisor's CV; Spanish names go in metadata. | 0010 |

--------------------------------------------------------------------------------

## Detailed Implementation Plan

### Conventions for all code

*   Python 3.13 (the owner's local version), same in CI. `sync/` and
    `checks/` are packages run from the repo root with `python -m`. Only
    dependencies: PyYAML, pypdf, Pillow, pinned to exact versions in
    `requirements.txt` (the latest release on the day of implementation).
*   Error format: `<file>[<index or line>]: <field>: <problem>`. Never the
    value, never a title (0009). Exit code 1 on any error, 0 otherwise.
*   Every write goes through one function that takes a dict
    `{relative_path: bytes}` and a list of allowed path patterns. It refuses
    the whole dict if any path matches no pattern, then writes each file to
    `<path>.tmp` and renames it.
*   Every generated text file starts with
    `<!-- GENERATED by sync/generate.py from <sources>. Do not edit. -->`
    (YAML files: the same text as a `#` comment).
*   Generated output: UTF-8, LF, keys in a fixed order, no timestamps.
*   Tests use the standard `unittest` module and fake data only. Fake leak
    values (DNI, phone, email) are built at run time from pieces (for
    example `"12" + "." + "345" + "." + "678"`), so no tracked file contains
    one.
*   Import direction: `checks/` may import `sync/` (schemas, generate).
    Library modules in `sync/` never import `checks/`; only the entry points
    (`sync/__main__.py` and the `main()` of `sync/strip.py`) call
    `checks.privacy` and `checks.binaries`.
*   Every reader of repo files takes a `read(path) -> bytes | None` function
    and a list of paths, never a repo root. `sync/files.py` provides the
    readers: disk, index (`git show :<path>`), commit
    (`git show <sha>:<path>`), and overlay (a dict laid over another
    reader).

### Order of work

Each step is committed only when its tests pass. No generated data is
committed before steps 1 to 3 exist (CLAUDE.md, Pending setup).

0.  Quarto spike, outside the repo (below).
1.  `checks/` and `.githooks/pre-commit`, `.githooks/pre-push`; enable the
    hooks; local hookify rules.
2.  `sync/schemas.py`, `sync/files.py`.
3.  `.claude/settings.json` deny rule; `.gitignore`; CLAUDE.md rules.
4.  `sync/generate.py`, then `sync/importer.py`, then `sync/__main__.py`.
5.  `sync/strip.py` (`strip_pdf` for the CV, `strip_image` for the
    headshot).
6.  Quarto shells, `_quarto.yml`, `_includes/person.html`; the owner creates
    `authored/home.md` and `authored/research.md`.
7.  `checks/postrender.py`.
8.  `.github/workflows/build.yml`, `requirements.txt`; set the Pages source.
9.  `README.md`, `LICENSE`, `LICENSE-CONTENT.md`.
10. Decision updates (0002, 0003, 0004, 0006, 0007, 0009) and CLAUDE.md
    "Where things stand".
11. First real `sync` against the vault export; first push.

**Phase 2 (decided 2026-11-26), built when the first item needs it**, each
part with its tests, in its own commit:

*   **CC BY abstracts**: `sync/abstract_license.py`,
    `data/abstract-licenses.yml`, `validate_abstract_licenses`, check 4,
    the `abstract` front matter key and the abstract on item pages.
*   **Hosted item files**: `files` entries with `path`, `resources` on item
    pages, and the `sync.strip` CLI destinations under
    `papers|talks|posters/<id>/`.

Until then the authored-file schema rejects `abstract` and `files[].path`,
so neither can reach the site unchecked. `files` entries with `url` and
`related` are built in phase 1. Parts below marked "(Phase 2)" wait.

### Step 0: Quarto spike (scratch directory, not committed)

A throwaway project with fake data, using Quarto 1.11.9. Each item has a
fallback, so no step later waits on a decision.

| # | Verify | Fallback if it fails |
| :--- | :--- | :--- |
| 1 | An explicit `render:` list renders only the listed `.qmd` files; `.md` files elsewhere are neither rendered nor copied. | Add `!design/`, `!docs/`, `!authored/` exclusions; the post-render check still guards. |
| 2 | A `table` listing reads `listing.yml` with custom fields, external `path` values and `sort: false`, keeping file order. | `type: default` with `description: <citation>`. |
| 3 | Markdown in a listing field (italic venue) renders. | Plain text venue. |
| 4 | `resources: [poster.pdf]` in front matter copies the file to `_site`. | A plain Markdown link to the file. |
| 5 | `quarto render -M last-updated:2026-11-25` sets metadata on a website render. | CI writes `_last-updated.yml`, listed under `metadata-files` in `_quarto.yml`. |
| 6 | `include-in-header: - text: '<meta ...>'` in front matter lands in `<head>`. | Write the tags to `<id>/_head.html` and use `include-in-header: _head.html`. |
| 7 | `{{< include /authored/home.md >}}` works while `authored/` is not rendered. | Move owner text to `authored/_home.md` (Quarto skips `_` files). |
| 8 | Sitemap URL form. | Record what Quarto writes; the post-render check normalises `/x/index.html` to `/x/`. |
| 9 | Default theme loads nothing from another site. | Set `theme: none` plus a small local CSS file. |
| 10 | `strip_pdf` (pypdf) run twice on the same input gives identical bytes. Not Quarto, but tested in the same spike. | `data/cv.yml` gains `source_sha256` (of the vault PDF as read), and "changed" is decided by that hash, not by the stripped bytes. |

Record the results in 0006 under "Tested" (step 10).

### Target Files to Create/Modify

#### 1. `checks/__init__.py` (Create)

*   **Type / Scope**: Python package marker.
*   **Proposed Changes**: Empty.

#### 2. `checks/privacy.py` (Create)

*   **Type / Scope**: Python module, used by the hooks, CI and `sync`.
*   **Proposed Changes**: `SCAN_SCOPE`, the path globs from the Technical
    Plan's Checks 2 (`data/**`, `authored/**`, `**/*.qmd`, `*/listing.yml`,
    `_quarto.yml`, `_includes/**`, `README.md`, `LICENSE*`), with
    `in_scope(path) -> bool`. `PATH_SCOPE` (`.claude/**`, `CLAUDE.md`,
    `.githooks/**`, `.github/**`, `.gitignore`, `.gitattributes`,
    `requirements.txt`), with `in_path_scope(path) -> bool`: only the
    absolute-path and username patterns run there.
    `scan_text(text, source_name, username=None, paths_only=False) ->
    list[str]`.
    *   First removes the exempt patterns: DOIs (`10\.\d{4,9}/\S+`), the ORCID
        format (`\d{4}-\d{4}-\d{4}-\d{3}[\dX]`), ISO dates.
    *   Then looks for:
        *   absolute paths (`[A-Za-z]:[\\/]`, `/Users/`, `/home/`, `~/`);
        *   DNI (`\b\d{2}\.?\d{3}\.?\d{3}\b`);
        *   CUIL (`\b\d{2}-?\d{8}-?\d\b`);
        *   any email address (`[\w.+-]+@[\w-]+(\.[\w-]+)*\.[A-Za-z]{2,}`);
        *   phone numbers: a `+54` prefix (`\+54[\s-]?\d`), or 8 or more
            digits in groups split by spaces or dashes
            (`\b\d{2,4}([\s-]\d{2,4}){2,}\b` with 8 or more digits in
            total); not applied to a `pages:` line in YAML;
        *   address words (case-insensitive `\b(calle|piso|depto|dpto)\b`);
        *   Argentine postal codes, CPA form only (`\b[A-Z]\d{4}[A-Z]{3}\b`).
    *   The exact regexes are fixed in the code; the test is that the sample
        export and the pages generated from it scan clean, and that each
        fake leak is still caught.
    *   If `username` is given, also looks for it and for the home path, as
        words, ignoring case.
    *   Returns `<source>:<line>: <kind>` only. The patterns live in one list
        at the top of the file.

#### 3. `checks/binaries.py` (Create)

*   **Type / Scope**: Python module.
*   **Proposed Changes**: `check_binary(path, data) -> list[str]`.
    *   Size at most 5 MB.
    *   PDF (pypdf): the Info dictionary holds no key other than `/Producer`;
        the root has no `/Metadata` (XMP); no `/EmbeddedFiles`; the text of
        every page goes through `privacy.scan_text`.
    *   JPEG and PNG (Pillow): no EXIF, no XMP, no PNG text chunks.
    *   Any other binary type is an error, so nothing unknown slips in.

#### 4. `checks/append_only.py` (Create)

*   **Type / Scope**: Python module.
*   **Proposed Changes**: `check_manifest(old, new)` and
    `check_ledger(old, new)`.
    *   Manifest: `new[:len(old)]` must equal `old` entry by entry, except
        that `withdrawn` may be added to an entry that lacked it.
    *   Ledger: every old line must still be present.
    *   `old` is read with `git show <ref>:<path>`. The check is skipped,
        with one line saying so, if there is no ref (first commit, a manual
        run, or CI with an all-zero `before`), or if the ref is not an
        ancestor of the checked commit (`git merge-base --is-ancestor`; a
        force push after an approved history rewrite, 2026-11-28). The local
        hooks still compare with `HEAD` or each commit's parent.

#### 5. `checks/__main__.py` (Create)

*   **Type / Scope**: CLI, `python -m checks [--staged | --commit <sha>]
    [--base <ref>] [--local]`.
*   **Proposed Changes**: Picks a reader and a file list:
    *   `--staged`: the index reader, and the files in
        `git diff --cached --name-only --diff-filter=ACMR` (the append-only
        and generate checks read every file they need through the same
        reader).
    *   `--commit <sha>`: the commit reader, and the files in
        `git ls-tree -r --name-only <sha>`; `--base` defaults to `<sha>^`.
    *   Neither: the disk reader, and `git ls-files`.

    `--local` (set by both hooks) adds the username check. Then it runs:
    1.  The schemas from `sync/schemas.py` on `data/items.yml` (through
        `sync/export_schema.validate_export`), `data/manifest.yml`,
        `data/cv.yml`, `data/abstract-licenses.yml` (Phase 2) and every
        `authored/**/*.md` front matter.
    2.  `privacy.scan_text` on every text file for which
        `privacy.in_scope` is true, and with `paths_only=True` on every
        file for which `privacy.in_path_scope` is true. The username is
        passed only with `--local`, taken from `getpass.getuser()` and
        `Path.home()`.
    3.  `binaries.check_binary` on every other file.
    4.  (Phase 2) The abstract-license rule: every authored `abstract` has a
        record whose `doi` equals the item's `doi` in `data/items.yml` and
        whose `url` matches `^https?://creativecommons\.org/licenses/by/`.
    5.  `append_only` against `HEAD` (`--staged`) or `--base`.
    6.  `sync.generate.check(read)` with the same reader.
    7.  With `--staged` only: error if `sync-pending.yml` exists on disk.

    It prints all errors, then exits 1 if there were any.

#### 6. `checks/postrender.py` (Create)

*   **Type / Scope**: CLI, `python -m checks.postrender _site`.
*   **Proposed Changes**:
    1.  Every line in `data/ledger.txt` maps to a file in `_site` (`/x/` →
        `x/index.html`). That file is a page or a tombstone (marker
        `data-tombstone` in the HTML).
    2.  Every `papers/*/index.html` that is not a tombstone has one
        `citation_title`, at least one `citation_author` and one
        `citation_publication_date`.
    3.  `sitemap.xml`, normalised (`/x/index.html` and `/x/` are the same),
        lists every built `index.html` that is not a tombstone.
    4.  `index.html` contains `Last updated \d{4}-\d{2}-\d{2}`.
    5.  No path under `_site` starts with `design/`, `docs/`, `data/`,
        `authored/`, `sync/` or `checks/`.
    6.  No `<script src>`, `<link href>` (stylesheet or font), CSS `@import`
        or `url()` in any built HTML or CSS points to another host.

#### 7. `checks/test_privacy.py`, `checks/test_binaries.py`, `checks/test_append_only.py`, `checks/test_postrender.py` (Create)

*   **Type / Scope**: Unit tests.
*   **Proposed Changes**:
    *   Privacy: each leak kind is caught; each exempt pattern (DOI, ORCID,
        date) is not; a year, a page range and a four-digit volume are not;
        the sample export scans clean; an absolute path in `CLAUDE.md` is
        caught; messages hold no matched text; `in_scope` is true for
        `data/items.yml` and `papers/x/index.qmd` and false for
        `checks/privacy.py` and `design/academic-website.md`.
    *   Binaries: a PDF built in the test with an Author field fails, and the
        same PDF after `sync/strip.py` passes; a JPEG with EXIF fails; a
        6 MB file fails; a PDF whose text holds a fake email fails.
    *   Append-only: removal, reordering and a changed `id` fail; adding
        `withdrawn` passes; a base that is not an ancestor skips with a
        message.
    *   Postrender: run against a tiny `_site` tree built in a temporary
        directory, with one case for each failure.

#### 8. `.githooks/pre-commit` (Create)

*   **Type / Scope**: POSIX shell script (Git for Windows runs it with its
    own `sh`).
*   **Proposed Changes**: `exec python -m checks --staged --local`. It must
    be executable (`git update-index --chmod=+x`).

#### 8a. `.githooks/pre-push` (Create)

*   **Type / Scope**: POSIX shell script, like the pre-commit hook.
*   **Proposed Changes**: For each `<local sha> <remote sha>` line that git
    passes on standard input (skipping deletions), list the new commits
    with `git rev-list <local> --not --remotes` and run
    `python -m checks --commit <sha> --local` on each. Any failure stops
    the push. Executable, like the pre-commit hook.

#### 9. `sync/__init__.py` (Create)

*   **Type / Scope**: Package marker.
*   **Proposed Changes**: Empty.

#### 10. `sync/export_schema.py` (Modify)

*   **Type / Scope**: Python module.
*   **Proposed Changes**: Docstring only: note that it also validates
    `data/items.yml`. No rule changes.

#### 11. `sync/test_export_schema.py` (Modify)

*   **Type / Scope**: Unit tests.
*   **Proposed Changes**: `import export_schema as es` becomes
    `from sync import export_schema as es`, so tests run from the repo root.
    Nothing else changes.

#### 12. `sync/schemas.py` (Create)

*   **Type / Scope**: Python module.
*   **Proposed Changes**: Validators in the same style as
    `export_schema.py` (they return a list of errors and reject unknown
    keys). `UID_RE` and `_valid_date` are imported from `export_schema.py`,
    not redefined, so the manifest's `uid` and dates follow the export's
    rules exactly.
    *   `validate_manifest`: a list of `{uid, type, id, withdrawn?}`. `type` is
        one of `papers`, `talks`, `posters`. The `id` regex is from the
        Technical Plan. `withdrawn` is a valid `YYYY-MM-DD`. `uid` and
        `(type, id)` are unique.
    *   `validate_authored`: front matter keys limited to `related` (list of
        `<type>/<id>`) and `files` (list of entries with `url`, `label` and
        `rights`, all non-empty strings). Phase 2 adds `path` as an
        alternative to `url` (`path` xor `url`; `path` has no `/` and no
        `..`) and `abstract` (string; papers only). Until then both are
        errors.
    *   `validate_cv`: `{date}` (plus `source_sha256` if Step 0 #10 fails).
    *   (Phase 2) `validate_abstract_licenses`: `{"papers/<id>": {url, doi,
        checked}}`.

#### 13. `sync/files.py` (Create)

*   **Type / Scope**: Python module.
*   **Proposed Changes**: `write_outputs(outputs, allowed)` as in
    Conventions. `read_front_matter(text) -> (dict, body)`, which splits a
    leading `---` YAML block. The four readers from Conventions:
    `disk_reader(root)`, `index_reader()`, `commit_reader(sha)`,
    `overlay_reader(outputs, base)`.

#### 14. `sync/generate.py` (Create)

*   **Type / Scope**: Python module and CLI, `python -m sync.generate
    [--check]`.
*   **Proposed Changes**: `build_outputs(read) -> dict[path, bytes]`,
    pure: it reads every input through `read` and nothing else.

    ```text
    items    = data/items.yml (validated)          by uid
    manifest = data/manifest.yml (validated)
    ledger   = data/ledger.txt lines (or empty)
    for entry in manifest:
        rec = items[entry.uid]           # missing -> error unless withdrawn
        if derived_type(rec) != entry.type: error
        auth = authored/<type>/<id>.md (optional, validated)
        has_page = body nonempty or files or abstract
        url = /<type>/<id>/
        if entry.withdrawn:
            if url in ledger: out[<type>/<id>/index.qmd] = tombstone(rec)
            continue                       # no row
        if url in ledger and not has_page: error "page lost its content"
        rows[type].append(row(rec, url if has_page else external(rec)))
        if has_page: out[<type>/<id>/index.qmd] = page(rec, auth, licenses)
    out[<type>/listing.yml] for each type (rows in items.yml order)
    out[cv/index.qmd] = cv_page(data/cv.yml if present)
    out[data/ledger.txt] = sorted(ledger ∪ FIXED_PAGES ∪ item pages)
    ```

    *   `FIXED_PAGES` = `/`, `/research/`, `/papers/`, `/talks/`,
        `/posters/`, `/cv/`.
    *   `derived_type`: `publication` → `papers`; `communication` with
        `format: poster` → `posters`; `oral` or `lecture` → `talks`.
    *   `related` targets must be in the manifest. Withdrawn targets are left
        out.
    *   (Phase 2) Each hosted `files.path` must exist in `<type>/<id>/`.
    *   **Display rules:**
        *   `date_display`: `12 Sep 2024`, `Sep 2024` or `2024`, by precision.
        *   `status_display`: `In press` or `Preprint`.
        *   Citation line: `Authors. Venue Volume, Pages.` for papers (venue
            in italics if Step 0 #3 passes); `Authors. Preprint.` for
            preprints; `Authors. Meeting. Abstract in <abstract_published_in>.`
            for talks and posters.
        *   `external()`: `https://doi.org/<doi>`, else `preprint_url`, else
            `url`, else no link.
    *   **Item page front matter:** `title`, `description` (the citation
        line), `resources` (hosted files, Phase 2), and `include-in-header`
        with the citation tags (papers only, as in the Technical Plan).
    *   **Item page body**, in this order: citation, status, links (DOI, free
        copy labelled by kind, preprint, `url`), summary, CC BY abstract with
        its label and license link (Phase 2), files with rights notes,
        related.
    *   **Tombstone:** title, `Withdrawn from this site on <date>.`, a
        `<div data-tombstone>`, nothing else.
    *   **CV page:** `[Curriculum vitae (PDF)](cv-public.pdf)`, `Updated
        <date>.` and `resources: [cv-public.pdf]`; or the placeholder line
        `The public CV will be posted here.`
    *   `check(read)`: build the outputs with `read` and compare each with
        `read(path)` for the same path; list every file that differs or is
        missing. `main(check)`: with `--check`, run `check(disk_reader)`.
        Without it, call
        `write_outputs` with allowed patterns `*/listing.yml`,
        `papers|talks|posters/*/index.qmd`, `cv/index.qmd`, `data/ledger.txt`.

#### 15. `sync/importer.py` (Create)

*   **Type / Scope**: Python module.
*   **Proposed Changes**: `import_export(vault_dir, read, pending) ->
    (outputs, pending_out, report)`. `pending` is the parsed
    `sync-pending.yml` or `None`; `pending_out` is the pending file to
    write, or `None` when every change is confirmed. It never prompts
    (2026-11-28).
    *   Load `<vault>/shared/cv/out/site-export.yaml` with
        `export_schema.load_export`.
    *   **Empty export:** if it has no items while the manifest has entries
        without `withdrawn`, error "export looks empty"; nothing else runs.
    *   **New IDs:** for each export record whose `uid` has no manifest
        entry, derive its type, then `suggest_id(record, taken)` by the rule
        under "ID suggestion" (Data formats). The surname is the part of
        the first `authors` entry before the initials. If both candidate
        tags are taken, the suggestion is `""`.
    *   **Missing items:** each manifest entry without `withdrawn` whose
        `uid` is absent from the export, with its title from the current
        `data/items.yml`.
    *   **Pending:** build the wanted pending entries (`new`, `missing`).
        Carry over `id` and `confirm` from `pending` for every `uid` still
        wanted; drop the others. Validate: only `id` and `confirm` may
        differ from what `sync` wrote; `confirm` is `yes`/`no` for `new`
        and `withdraw`/`no` for `missing`; each confirmed `id` matches the
        regex and is unique within its type.
    *   If anything is wanted and any entry is unconfirmed or invalid,
        return `pending_out` and no outputs (the caller writes only the
        pending file). Otherwise append `{uid, type, id}` for each `new`
        entry, add `withdrawn: <today>` for each `missing` entry, and return
        `pending_out = None`.
    *   For a manifest entry with `withdrawn`: if its `uid` is in the export,
        that is an error; otherwise keep its record from the current
        `data/items.yml`.
    *   Keep records whose `uid` is in the (updated) manifest; that is now
        every export record.
    *   Sort by `date` descending, then `uid`; write `data/items.yml`.
    *   **CV:** if `<vault>/shared/cv/out/cv-public.pdf` exists, strip it
        with `strip.strip_pdf` and compare with `cv/cv-public.pdf` (or, if
        Step 0 #10 fails, compare the source's SHA-256 with
        `data/cv.yml`'s `source_sha256`). If different, output the PDF and
        a `data/cv.yml` with today's date. If the file is missing, output
        nothing for the CV. The binary check runs in `sync/__main__.py`
        (step 4), not here.
    *   **Report:** counts of kept, withdrawn kept, new IDs, newly
        withdrawn, and the CV state (`none`, `unchanged`, `updated`).

#### 16. `sync/__main__.py` (Create)

*   **Type / Scope**: CLI, `python -m sync [--dry-run]`.
*   **Proposed Changes**:
    1.  Fail unless `git config core.hooksPath` is `.githooks`.
    2.  Fail unless `VAULT_DIR` is set and points to an existing folder.
    3.  Read `sync-pending.yml` if it exists and run `importer`. If it
        returns a pending file: unless `--dry-run`, write it with
        `write_outputs` (allowed: `sync-pending.yml`), print "N entries need
        your confirmation in sync-pending.yml; nothing else was written"
        and exit 1. `--dry-run` prints the counts and exits 0. Otherwise
        delete any old `sync-pending.yml` after step 6 succeeds, and run
        `generate.build_outputs` with
        `overlay_reader(import outputs, disk_reader)`, the repo as it would
        be after the import.
    4.  Run `privacy.scan_text` on every text output and
        `binaries.check_binary` on the PDF. Any error stops the run before
        anything is written.
    5.  Print the report: rows, pages and tombstones per type; new IDs;
        newly withdrawn; CV state.
    6.  Unless `--dry-run`, write the import outputs, then the generate
        outputs, each through `write_outputs` with its own allowed list
        (import: `data/manifest.yml`, `data/items.yml`, `data/cv.yml`,
        `cv/cv-public.pdf`).

#### 17. `sync/abstract_license.py` (Create, Phase 2)

*   **Type / Scope**: CLI, `python -m sync.abstract_license papers/<id>`.
*   **Proposed Changes**:
    1.  Read the item's `doi` from `data/items.yml`, through the manifest.
    2.  `GET https://api.crossref.org/works/<doi>` with User-Agent
        `site-abstract-license-check/1.0`, no email, a 20-second timeout.
    3.  Accept the first `message.license[]` entry whose `content-version`
        is `vor` or `unspecified`, whose `URL` matches the CC BY pattern and
        whose `start` date is on or before today.
    4.  Write `papers/<id>: {url, doi, checked: today}` into
        `data/abstract-licenses.yml` with `write_outputs` (allowed: that one
        path).
    5.  Any other result: print `not CC BY` or `no license data`, write
        nothing, exit 1.

    The response parsing is a separate function, so tests use saved JSON
    and make no network call.

#### 18. `sync/strip.py` (Create)

*   **Type / Scope**: Module and CLI, `python -m sync.strip <src> <dest>`.
*   **Proposed Changes**:
    *   `strip_pdf(data) -> bytes`: pypdf, clone all pages into a new writer,
        no Info except `/Producer`, no XMP, no embedded files.
    *   `strip_image(data, kind) -> bytes`: Pillow, copy the pixels into a
        new image, save with no EXIF, XMP or text chunks (JPEG quality 95).
    *   CLI: `<src>` must be under `staging/`. `<dest>` must be
        `images/headshot.jpg` (Phase 2 adds
        `papers|talks|posters/<id>/<name>`). After stripping, it runs
        `binaries.check_binary`, then writes.
    *   Phase 2, for hosted PDFs: `strip_pdf` also drops annotations, and a
        PDF with images but no extractable text is refused unless
        `--image-only-ok` is given by the owner.

#### 19. `sync/test_generate.py`, `sync/test_importer.py`, `sync/test_schemas.py`, `sync/test_abstract_license.py`, `sync/test_strip.py` (Create)

*   **Type / Scope**: Unit tests. Fixtures are built in temporary
    directories from `design/site-export.sample.yaml`; no fixture `.qmd`
    files are committed.
*   **Proposed Changes**:
    *   Generate: a row-only item; an item with a summary gets a page and a
        ledger line; (Phase 2) a CC BY abstract with and without a license
        record; a type mismatch error; with the index reader, a partly
        staged change is checked against the staged inputs only; a page in the ledger that lost its content
        errors; a withdrawn item with a page gets a tombstone; a withdrawn
        row-only item loses its row; `related` to a withdrawn item is left
        out; a preprint published in place keeps its URL and moves in order;
        running `build_outputs` twice gives identical bytes; `--check`
        reports a hand-edited page.
    *   Importer: every error row of the Lifecycle table; CV missing,
        unchanged and updated. With pending files built in the test: a new
        item writes a pending file and no outputs; `confirm: yes` appends
        the entry; an edited `id` is used; a bad or duplicate `id` stops
        with the pending file kept; a clash gets the next title word, and a
        double clash gives an empty `id`; `2D` is skipped; accented and
        compound surnames; a missing item is withdrawn on `withdraw` and
        refused on `yes`; an edited `uid` or `title` is an error; a changed
        export keeps the answers that still apply; an empty export with
        live manifest entries stops before any pending file.
    *   Schemas: each rule accepts and rejects.
    *   (Phase 2) Abstract license: saved Crossref replies for CC BY
        (`vor`), CC BY-NC, a `tdm` license only, and no license.
    *   Strip: output has no metadata and the same page count.

#### 20. `_quarto.yml` (Create)

*   **Type / Scope**: Quarto project config.
*   **Proposed Changes**:
    *   `project`: `type: website`, `output-dir: _site`, and `render:` set to
        exactly `index.qmd`, `research/index.qmd`, `cv/index.qmd`,
        `papers/**/*.qmd`, `talks/**/*.qmd`, `posters/**/*.qmd`, so no stray
        `.qmd` anywhere else can become a page.
    *   `website`:
        *   `title: Abraham Yeffal`, `site-url: https://ayeffal.github.io/`,
            `search: false`.
        *   navbar: Home `/`, Research `/research/`, Papers `/papers/`, menu
            "Talks and posters" (Talks `/talks/`, Posters `/posters/`), CV
            `/cv/`.
        *   `page-footer`: `ayeffal (at) unsam (dot) edu (dot) ar` · "Content
            CC BY 4.0" linked to `https://creativecommons.org/licenses/by/4.0/`
            · "Code MIT" linked to the repo's `LICENSE` on GitHub.
    *   `format: html` with the default theme.
    *   `last-updated: "local preview"`, which CI overrides.

#### 21. `index.qmd` (Create)

*   **Type / Scope**: Home page shell (Claude-written, owner-reviewed).
*   **Proposed Changes**:
    *   Front matter: `title: Abraham Yeffal` and `include-in-header:
        _includes/person.html`.
    *   Body: the two affiliation lines from 0010, then
        `{{< include /authored/home.md >}}`, then links to ORCID
        (`https://orcid.org/0000-0002-9645-6664`) and Scholar (the 0010 URL),
        then `Last updated {{< meta last-updated >}}`.
    *   The headshot line (`images/headshot.jpg`, with alt text) is added in
        the same commit as the image.
    *   After the site is live, the Search Console verification `<meta>` tag
        is added to `include-in-header` (0010).

#### 22. `_includes/person.html` (Create)

*   **Type / Scope**: Static HTML snippet.
*   **Proposed Changes**: A JSON-LD `Person` block:
    *   `name`: Abraham Yeffal;
    *   `sameAs`: the ORCID and Scholar URLs;
    *   `affiliation`: CONICET; UBA School of Medicine, with
        `alternateName` *Facultad de Medicina, Universidad de Buenos Aires*;
        ICIFI, ECyT, UNSAM, with `alternateName` *Instituto de Ciencias
        Físicas (ICIFI), Escuela de Ciencia y Tecnología (ECyT), Universidad
        Nacional de San Martín (UNSAM)*.

    No email.

#### 23. `research/index.qmd` (Create)

*   **Type / Scope**: Research page shell.
*   **Proposed Changes**: `title: Research`;
    `{{< include /authored/research.md >}}`; the "In Spanish" line with the
    Spanish official names from 0010.

#### 24. `papers/index.qmd`, `talks/index.qmd`, `posters/index.qmd` (Create)

*   **Type / Scope**: List page shells.
*   **Proposed Changes**: Each has its title (Papers, Talks, Posters) and a
    `listing:` block with:
    *   `contents: listing.yml`, `type: table`, `sort: false`;
    *   `fields: [date_display, title, citation, status_display, page]` and
        display names (`Date`, `Title`, `Details`, `Status`, `Page`);
    *   `filter-ui: false`, `sort-ui: false`;
    *   or the Step 0 fallback.

    The talks page links to `/posters/` and the posters page to `/talks/`.

#### 25. `papers/listing.yml`, `talks/listing.yml`, `posters/listing.yml`, `cv/index.qmd`, `data/ledger.txt`, `data/items.yml` (Create, generated)

*   **Type / Scope**: Tool files.
*   **Proposed Changes**: Written by the first `sync` run (step 11). Before
    any real item exists, `python -m sync` runs against the real export,
    which is currently `items: []`. That gives empty listings, the
    placeholder CV page and a ledger of the fixed pages.

#### 26. `data/manifest.yml` (Create)

*   **Type / Scope**: Tool file, written by `sync` import after the owner
    confirms in `sync-pending.yml`.
*   **Proposed Changes**: Created by Claude as `[]` with a header comment
    saying it is written by `sync` and describing the entry format, before
    the deny rule goes in (step 3). From then on, only `sync` writes it.

#### 27. `authored/home.md`, `authored/research.md` (Create, by the owner)

*   **Type / Scope**: Owner text.
*   **Proposed Changes**: The owner moves the text from
    `design/home-research-text.md`. The home paragraph goes to
    `authored/home.md`. `authored/research.md` gets the research text. The
    "Methods and tools" list stays out until the owner confirms it. Claude
    does not write these files.

#### 28. `design/home-research-text.md` (Delete)

*   **Type / Scope**: Design note.
*   **Proposed Changes**: Deleted after the owner confirms that the text is
    in `authored/`, so the text is not kept in two places.

#### 29. `.github/workflows/build.yml` (Create)

*   **Type / Scope**: GitHub Actions workflow.
*   **Proposed Changes**: Triggers: push to `main`, and
    `workflow_dispatch`.
    *   **Job `check`:**
        1.  `actions/checkout` with `fetch-depth: 0`.
        2.  `actions/setup-python` with 3.13, then `pip install -r
            requirements.txt`.
        3.  `python -m unittest discover -t . -s sync` and the same for
            `checks`.
        4.  `python -m checks --commit HEAD --base ${{ github.event.before }}`.
    *   **Job `build`** (needs `check`):
        1.  `quarto-dev/quarto-actions/setup` with `version: 1.11.9`.
        2.  `quarto render -M last-updated:$(git log -1 --format=%cs --
            data authored '*.qmd')`.
        3.  `python -m checks.postrender _site`.
        4.  `actions/upload-pages-artifact` with `path: _site`.
    *   **Job `deploy`** (needs `build`, runs only on `refs/heads/main`):
        `actions/deploy-pages`.

    Permissions are `contents: read`, `pages: write`, `id-token: write`, with
    one `pages` concurrency group. Each action is pinned to a release tag.
    CI runs `python -m checks --commit HEAD --base <before>`, the same code
    the pre-push hook runs, so the hook tests cover it.

#### 30. `requirements.txt` (Create)

*   **Type / Scope**: Dependency pins.
*   **Proposed Changes**: `PyYAML==<x>`, `pypdf==<x>`, `Pillow==<x>`. Exact
    versions are chosen on the day of implementation and are also used
    locally.

#### 31. `.gitignore` (Modify)

*   **Type / Scope**: Git config.
*   **Proposed Changes**: Add `__pycache__/`, `.venv/`,
    `.claude/*.local.md` (the local hookify rules) and `sync-pending.yml`.

#### 32. `.claude/settings.json` (Modify)

*   **Type / Scope**: Claude Code project settings (tracked).
*   **Proposed Changes**: Add `permissions.deny`: `Edit(authored/**)`,
    `Write(authored/**)`, `Edit(data/manifest.yml)`,
    `Write(data/manifest.yml)`, `Edit(sync-pending.yml)`,
    `Write(sync-pending.yml)`. No machine-specific paths.

#### 33. `.claude/hookify.owner-files.local.md`, `.claude/hookify.hook-bypass.local.md` (Create, local, untracked)

*   **Type / Scope**: Hookify rules (CLAUDE.md Pending setup).
*   **Proposed Changes**:
    *   The first rule blocks any Bash command that writes to `authored/`,
        `data/manifest.yml` or `sync-pending.yml` (redirections, `sed -i`,
        `cp`, `mv`, `tee`, `rm`).
    *   The second rule blocks the ways Claude could get past the git hooks:
        `--no-verify` on `git commit` or `git push`, any
        `git config core.hooksPath`, and writes to `.githooks/`. It holds no
        privacy patterns: those live only in `checks/privacy.py`, so they
        cannot drift apart (2026-11-26).
    *   Both rules are created with the hookify plugin's own commands, not by
        hand.

#### 34. `CLAUDE.md` (Modify)

*   **Type / Scope**: Project instructions.
*   **Proposed Changes**:
    *   Add to Rules: "Never write `authored/**`, `data/manifest.yml` or
        `sync-pending.yml`; propose text in chat." and "Never edit generated
        files. New IDs and withdrawals are confirmed only by the owner, in
        `sync-pending.yml`."
    *   Update "Where things stand".
    *   Remove each Pending setup line once it is done.
    *   Add "Set `VAULT_DIR` (value in CLAUDE.local.md)" to the setup notes.

#### 35. `CLAUDE.local.md` (Modify, local, untracked)

*   **Type / Scope**: Machine notes.
*   **Proposed Changes**: The value of `VAULT_DIR` (the vault root) and the
    one-time `setx VAULT_DIR ...` command.

#### 36. `README.md` (Create)

*   **Type / Scope**: Repo docs (not rendered: it is not in `render:`).
*   **Proposed Changes**: Covers:
    *   what the repo is;
    *   setup from a fresh clone: Python 3.13, `pip install -r
        requirements.txt`, Quarto 1.11.9, `git config core.hooksPath
        .githooks`, `VAULT_DIR`;
    *   the commands `sync`, `sync --dry-run`, `sync.strip`,
        `quarto preview`, the tests (and `sync.abstract_license` in
        Phase 2);
    *   the seven "Adding an item" steps;
    *   the "Who writes what" table, linked to this design.

#### 37. `LICENSE` (Create)

*   **Type / Scope**: MIT License.
*   **Proposed Changes**: Copyright "Abraham Yeffal", with the year of first
    publication (0007).

#### 38. `LICENSE-CONTENT.md` (Create)

*   **Type / Scope**: Content license notice.
*   **Proposed Changes**:
    *   The owner's text is CC BY 4.0, with a link to the license.
    *   CC BY abstracts carry their own license and source.
    *   Third-party files are covered by neither license; each shows its own
        rights note (0007).

#### 39. `docs/decisions/0002-url-scheme.md`, `0003-item-ids.md`, `0004-data-schema.md`, `0006-site-generator.md`, `0007-licenses.md`, `0009-privacy-and-permanence.md` (Modify)

*   **Type / Scope**: Decision records, updated after the design is
    approved.
*   **Proposed Changes**: As listed in "Decision updates this plan needs":
    *   0002: the `aliases:` safety net is withdrawn, pages do not move, and
        the ledger holds page URLs only.
    *   0003: `sync` suggests IDs, confirmed in `sync-pending.yml`; the year
        is the year of `date` when the ID is made.
    *   0004: the license record moves to `data/abstract-licenses.yml`;
        `related` and `files` live in the authored front matter; visibility
        is the vault consent plus the owner's ID confirmation.
    *   0006: the two-step `sync`; CI reruns `generate --check`; the CV
        reason has lapsed; the Step 0 results go under "Tested".
    *   0007: the license record's location; the `start` date rule.
    *   0009: `build` runs `generate --check`; the local hooks are the
        privacy gate for what reaches GitHub; the pre-push hook; `sync`
        refuses to run without the hooks; `sync` does not finish while an
        exported item has no ID; withdrawals confirmed with `withdraw`; CI's
        append-only baseline.

    Each change is dated 2026-11-25 or later.

#### 40. `images/headshot.jpg`, hosted item files (Create, when the owner provides them)

*   **Type / Scope**: Owner-provided binaries.
*   **Proposed Changes**: These are always added through `python -m
    sync.strip staging/<file> <dest>`, and only when the owner names the
    file (0004).

### Verification Plan

*   **Compilation/Build**: `quarto render` (local and CI, Quarto 1.11.9).
*   **Unit Tests**: these cover the pre-push hook's checks and CI's, since
    both run `python -m checks --commit`. Commands:
    `python -m unittest discover -t . -s sync` and
    `python -m unittest discover -t . -s checks`, run locally and in CI.
*   **Static Analysis & Linting**: none added (no unrequested
    dependencies); `python -m checks` is the repo's own static check.
*   **Test Coverage Requirement**: every row of the Lifecycle table and
    every check in `checks/` has at least one passing and one failing test.
    No percentage target, since that would need a coverage tool.
*   **E2E/Integration**:
    1.  **Fake vault.** Copy `design/site-export.sample.yaml` into a scratch
        folder as `shared/cv/out/site-export.yaml` and set `VAULT_DIR` to
        it. In a scratch clone (never committed), run `sync`, set
        `confirm: yes` for the five suggested IDs in `sync-pending.yml`, and
        run `sync` again. Then run `quarto render` and
        `checks.postrender`, and confirm rows, pages, a tombstone and the
        sitemap.
    2.  **Hook leak test.** In a scratch clone, stage one file per leak kind
        (fake values) and a PDF with metadata. Each commit is refused.
    3.  **Bypass test.** In the same scratch clone, with a local bare repo as
        its `origin`, commit one fake leak with `--no-verify` and push. The
        pre-push hook refuses the push. Nothing is pushed to GitHub. This
        replaces the earlier CI leak test (2026-11-26), which would have
        published a fake leak in the public repo's history.
    4.  **Ledger test.** In a scratch clone, delete a generated page for a
        ledger URL. `generate --check` and `checks.postrender` both fail.
    5.  **Fresh clone.** The first push to `main` builds and deploys from a
        clean checkout (the Zero cost, no lock-in goal).
    6.  **Timed walkthrough.** Add the first real item following "Adding an
        item" and record the minutes (the 10-minute goal).

--------------------------------------------------------------------------------

*Drafted with EGM*
