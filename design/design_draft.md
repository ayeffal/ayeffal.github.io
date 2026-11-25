# Academic website

*   **Author:** Abraham Yeffal
*   **Status:** Draft (Overview & Goals approved 2026-11-25; Technical Plan
    approved 2026-11-25; Alternatives approved 2026-11-25; Detailed Implementation drafted, awaiting
    review)
*   **Date:** 2026-11-24

--------------------------------------------------------------------------------

## Overview

A personal academic website at `https://ayeffal.github.io/`, hosted on GitHub
Pages, for a PhD candidate in neuroscience in Argentina. It has five pages:
Home, Research, Papers, Talks and posters, and CV (0010).

The data comes from a private notes vault. A program in a separate private
vault-side repository writes one export file holding only papers, talks and
posters that the owner has marked public there, and only allowlisted fields
(0008). In this repo, a local script, `sync`, reads that file and writes
committed data files. An automatic `build` in GitHub Actions turns the
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
"Superseded lines in the brief" below).

## The Problem

The owner needs one public page that search committees, editors and
collaborators find when they look up the name "Abraham Yeffal", and that
joins the owner's papers, talks, ORCID, Google Scholar profile and
affiliations. No such page exists.

Three things make this harder than a plain personal page:

1. **The records are private.** Papers, talks and posters are recorded in a
   private vault that also holds unpublished manuscripts, ID numbers,
   requirement points and personal notes. Copying from it by hand is slow and
   one mistake can publish something that git history then keeps forever.
2. **The same records feed the PDF CV.** If the site and the CV are kept
   separately, they drift apart.
3. **Links must not break.** GitHub Pages cannot do server-side redirects, and academics
   paste links to single items into CVs, forms and papers. A URL that moves
   or disappears breaks every saved copy.

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
    list the same papers, talks and posters, because both use the vault's one
    eligibility rule (0008, 0010). Check: the build fails if the home page
    lacks the last-updated date.
*   **One source of truth.** Every paper, talk and poster shown on the site
    comes from the vault export. This repo adds only the owner's authored
    text (or a CC BY paper's abstract), the `id`, `related` links and `files`
    entries (0004). Check: `sync` is the only program that writes item data,
    and it reads only the export and the public CV PDF.
*   **Private by construction.** No commit and no deploy goes through if the
    committed data holds a key not on the allowlist, an absolute path, a
    username, a DNI/CUIL pattern, the plain form of the contact email, a phone
    number or an address. The public CV PDF's text gets the same scan before
    `sync` writes it (0008). The same checks run before each commit and
    again in the automatic build (0009). Committed PDFs and images (the CV,
    hosted files, the headshot) have their metadata stripped (0004, 0008,
    0010). Check: a test commit with each kind of leak, including a file with
    metadata, is refused by both.
*   **Permanent URLs.** Any link to an item or page that has ever been
    shared keeps reaching that item or page. GitHub Pages cannot do
    server-side redirects, so URLs are chosen with foresight to never need changing, and an ID is
    never reused for a different item (0002). Check: the build fails if any
    URL in the committed ledger (the list of every URL ever published) has
    none of: a page, a tombstone (a page left at the URL saying the item was
    withdrawn), or a Quarto `aliases:` redirect to the page's new address,
    used only as a safety net when a page has to move.
*   **Zero cost, no lock-in.** The site builds from a fresh clone with pinned
    Quarto (pinned to 1.11.9, not yet tested) and Python, and uses no paid service (0006).
    Check: a CI build from a clean checkout succeeds.
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

### Settled during drafting (2026-11-24)

These go into the Technical Plan.

*   **Status spelling.** Data keeps the export's value `in-press`; pages show
    "In press".
*   **List order.** Lists sort by the item's current `date`, the export's own
    order (`date` descending, then `uid`). A preprint that is published moves
    to its publication date. Its ID and URL do not change.
*   **`author_position`** stays out of the site (0004, resolved).
*   **Withdrawal** uses a `withdrawn` date in the manifest (0009). An item
    with a page becomes a tombstone; an item with only a list row loses its
    row. The manifest entry stays, so the ID is never reused.
*   **Public CV PDF.** `sync` copies it from a fixed vault-side path, strips
    its metadata and scans its text before writing it (0008). Agreed path:
    `shared/cv/out/cv-public.pdf`. No CV builder exists yet, so a missing
    file means "no CV yet": `sync` skips it and the CV page is a placeholder.
*   **Search Console.** Register with Google Search Console and import into
    Bing Webmaster Tools, once the site is live (0010).
*   **Quarto `aliases:`** is the safety net for a page that has to move: it
    writes a JavaScript redirect file at the old path, which GitHub Pages
    serves. Stable URLs stay the rule; tombstones stay for withdrawals (0002).
*   **Co-author removal request.** A published author list is public record,
    so citations stay as published. The co-author's name is removed from the
    owner's own text and hosted files, and a hosted file they co-own is taken
    down (its URL becomes a tombstone).
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
    added; the license URL, DOI and check date are recorded in the authored
    file, and the build (offline) fails if they are missing or not CC BY. A
    summary is optional: a missing one is never an error and never blocks
    `sync`, the build or the item's list row.
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
    row first, then pages one item at a time ("Adding an item").
*   "A program in the vault repo writes one export file." Current: a
    separate private vault-side repository (`vault-export`) writes it
    (reply 1, reply 3).

## Technical Plan (Architecture)

### Settled before drafting (2026-11-25)

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

### Terms

*   **CI**: GitHub Actions. On each push to `main`, GitHub starts a fresh
    temporary machine, downloads the repo, installs the pinned Quarto and
    Python, runs the checks, builds the site and publishes it. If any check
    fails, nothing is published and the previous site stays up. Free for
    public repos.
*   **Owner file**: a file only the owner writes. **Tool file**: a file only
    a program writes. No file is both (see "Who writes what").

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
 │ import:  export ──validate──► keep only manifest uids             │
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
papers/<id>/<file>.pdf      owner-added hosted file (optional, <= 5 MB)
talks/ ... posters/ ...     same shape as papers/
cv/index.qmd                GENERATED: CV page or placeholder
cv/cv-public.pdf            written by sync import (absent until a CV exists)
authored/home.md            OWNER: home text
authored/research.md        OWNER: research text
authored/<type>/<id>.md     OWNER: an item's summary, related, files, abstract
authored/<type>/<id>.es.md  OWNER, later: Spanish text (0001); not built yet
images/headshot.jpg         owner-added, metadata stripped
data/manifest.yml           OWNER: one entry per public item (append-only)
data/items.yml              written by sync import: export records kept
data/cv.yml                 written by sync import: date of the current CV
data/abstract-licenses.yml  written by the abstract-license tool only
data/ledger.txt             written by generate: every URL ever published
sync/                       export_schema.py (exists), sync, generate,
                            abstract-license tool, metadata-strip tool, tests
checks/                     pre-commit and CI checks, post-render checks, tests
.githooks/pre-commit        runs checks on the staged files
.github/workflows/build.yml CI: checks, generate --check, render, deploy
requirements.txt            pinned Python packages
LICENSE, LICENSE-CONTENT.md MIT for code; CC BY 4.0 notice for content (0007)
```

Quarto renders only `.qmd` files (`render: ["**/*.qmd"]` in
`_quarto.yml`), so the `.md` files in `authored/`, `design/` and `docs/`
never become pages. A post-render check makes sure of it (below). Every
page lives at `<dir>/index.qmd`, so it builds to `<dir>/index.html` and is
reached at `<dir>/`, as 0002 requires.

### Who writes what

| File | Written by | Never written by |
| :--- | :--- | :--- |
| `authored/**`, `data/manifest.yml` | owner | any program; Claude |
| `data/items.yml`, `data/cv.yml`, `cv/cv-public.pdf` | `sync` import | owner, Claude |
| generated pages, `listing.yml`, `data/ledger.txt` | `generate` | owner, Claude |
| `data/abstract-licenses.yml` | abstract-license tool | owner, Claude |
| hosted files, headshot | metadata-strip tool, from a copy the owner puts in `staging/` (gitignored) | `sync` |
| shells, `_quarto.yml`, code, workflow | Claude, reviewed by owner | `sync` |

Guards:

*   Each program has a fixed list of paths it may write and refuses any
    other path. The owner's files are on no list.
*   Every generated file starts with a comment saying it is generated and
    naming its source. A hand edit is caught by `generate --check` in the
    pre-commit hook and in CI.
*   `.claude/settings.json` (tracked) denies Claude's Edit and Write tools on
    `authored/**` and `data/manifest.yml`. A deny rule does not cover shell
    commands, so the hookify rule (Pending setup in CLAUDE.md) also blocks
    shell writes to those paths. Claude proposes text changes in chat and the
    owner makes them.
*   **Change to 0004 (proposed here):** the CC BY license record (`url`,
    `doi`, `checked` date) moves out of the owner's authored file into
    `data/abstract-licenses.yml`, keyed by `<type>/<id>`. That way no program
    ever writes into a file the owner wrote. The abstract text itself stays
    in the owner's file.

### Data formats

**`data/manifest.yml`** (owner, append-only). A list of entries:

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
  - path: "poster.pdf"                # hosted, in <type>/<id>/
    label: "Poster (PDF)"
    rights: "© the authors"           # one-line rights note (0007)
  - url: "https://zenodo.org/..."     # external, e.g. a recording
    label: "Recording"
    rights: "© the authors"
abstract: |                           # papers only; CC BY abstract, copied
  ...                                 # by the owner from the publisher
```

The body is the summary in the owner's words. Any other front matter key
is an error.

**`data/abstract-licenses.yml`** (tool). `papers/<id>: {url, doi,
checked}`. Written by `sync/abstract-license` after it asks Crossref for the
item's DOI (taken from `data/items.yml`) and finds a license entry for the
published version (or with an unspecified version) whose URL starts with
`http(s)://creativecommons.org/licenses/by/`. The request sends a generic
User-Agent and no email. The tool refuses to write anything for any other
license.

**`data/cv.yml`** (sync import). `date: "YYYY-MM-DD"`, the day `sync` last
wrote a changed CV PDF. Absent until a CV exists.

**`data/ledger.txt`** (generate). One site path per line, for example
`/papers/surname-2026-tag/` or `/posters/surname-2024-tag/poster.pdf`.
`generate` writes the old lines plus every page and hosted file it now
produces, sorted. A line is never removed.

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
    manifest's `type`, it is an error. The owner then decides whether the
    page moves (with a Quarto `aliases:` entry, 0002) or the export is fixed.
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
    (untested) and add a citation box nobody asked for.
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
| Owner marks an item public in the vault | The export counts it as "not in manifest" until the owner adds the manifest entry. |
| Manifest entry added | Next `sync` adds its record and a row; a page too if an authored file has content. |
| Preprint is published | Same `uid`, so the same ID and URL. The record updates in place, the row moves to the new date, and the summary stays. |
| Authored file gains content | The row gets a page; its URL enters the ledger. |
| Page loses all content (authored file emptied or deleted) | Error: the URL is in the ledger. The owner restores the content or withdraws the item. |
| Manifested item missing from the export, not withdrawn | Error (0009). |
| Item marked `withdrawn` but still in the export | Error (0009). |
| Item withdrawn | Tombstone if it had a page; otherwise the row goes. The manifest entry stays. |
| `related` names an item not in the manifest | Error. |
| Export `schema_version` is not 1 | Error, nothing written (0003). |
| CV PDF appears or changes | Stripped, scanned, written with a new `data/cv.yml` date. A failed scan stops `sync`. |
| CV PDF unchanged apart from metadata | Nothing written. |

`sync` computes every output and runs every check in memory before writing
anything, then writes each file through a temporary file and a rename. Its
report gives counts only (`N rows, N pages, N tombstones, N not in
manifest`), never titles or values (0009). `--dry-run` prints the report and
writes nothing. `sync` refuses to run if `git config core.hooksPath` is not
`.githooks`, so the pre-commit hook cannot be silently inactive.

### Checks

**`checks`** run in the pre-commit hook (on the staged version of each
file) and again in CI (on the pushed commit):

1.  **Allowlist.** `data/items.yml` passes `sync/export_schema.py`;
    `data/manifest.yml`, `data/cv.yml`, `data/abstract-licenses.yml` and the
    authored front matter pass their own schemas, which reject unknown keys.
2.  **Privacy scan** of every tracked text file: absolute paths
    (`X:\`, `/Users/`, `/home/`), DNI and CUIL patterns, any email address in
    plain form, phone-number patterns, and street-address words (`calle`,
    `piso`, `depto`, Argentine postal codes). The username check runs only in
    the pre-commit hook, using the machine's current username and home path,
    because the username is in no tracked file and CI cannot know it.
    Known false positives (the ORCID iD, DOIs, `YYYY-MM-DD` dates) are exempt
    by pattern, in one list in the code. Error messages name file and line,
    never the matched text.
3.  **Binary files**: every committed PDF and image is at most 5 MB and has
    no metadata (PDF Info dictionary and XMP; image EXIF and XMP). Each PDF's
    text is extracted and gets the scan in 2. A poster that prints co-author
    emails is therefore refused until the emails are removed.
4.  **Abstracts**: every authored `abstract` has an entry in
    `data/abstract-licenses.yml` whose `doi` matches the item and whose URL
    is CC BY. No network call.
5.  **Append-only**: the manifest and the ledger, compared with `HEAD` in
    the hook and with the previously pushed commit in CI.
6.  **`generate --check`**: regenerate in memory and compare with the
    committed generated files; any difference fails.

**Post-render checks** (CI only, after `quarto render`):

*   Every ledger path exists in `_site` as a page, a tombstone or a Quarto
    alias redirect file. This is checked on the built file, because Quarto
    silently skips an alias that would overwrite a page (0002).
*   Every non-tombstone paper page has `citation_title`, `citation_author`
    and `citation_publication_date`.
*   `sitemap.xml` lists every built page except alias redirect files.
*   The home page shows "Last updated YYYY-MM-DD". CI passes the date of the
    last commit to Quarto as metadata (`-M`); the home shell prints it.
*   `_site` holds nothing from `design/`, `docs/`, `data/`, `authored/`,
    `sync/` or `checks/`.
*   No third-party requests: no built HTML or CSS loads a script, style or
    font from another site. Links are allowed. This is why the site uses
    Quarto's default Bootstrap theme: some Bootswatch themes import Google
    Fonts.

**What the hook cannot do.** The repo is public. Once a commit is pushed,
GitHub shows it, whatever CI decides; CI can stop the deploy, not the
exposure. The pre-commit hook is therefore the real privacy gate, and CI is
the backstop for the deploy. GitHub offers no server-side hook that could
refuse a push on github.com.

### Site configuration

*   `_quarto.yml`: website project, `site-url: https://ayeffal.github.io/`,
    `output-dir: _site`, `render: ["**/*.qmd"]`, default theme, search
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

On push to `main`: check out with full history (needed for the
append-only check), set up Python 3.12 and install the pinned
`requirements.txt` (PyYAML, pypdf, Pillow), run `checks` and
`generate --check`, install Quarto 1.11.9 with `quarto-dev/quarto-actions`,
render with the last-commit date, run the post-render checks, then upload
`_site` and deploy with GitHub's Pages actions. One-time manual step: set
the repo's Pages source to "GitHub Actions".

### Adding an item (the 10-minute path)

1.  In the vault: mark the item public; run the vault-side export.
2.  Add its manifest entry (`uid` from the vault note, `type`, a new `id`).
3.  Optional: write `authored/<type>/<id>.md`. For a CC BY abstract, paste
    it and run the abstract-license tool.
4.  Optional: put a file in `staging/`, run the metadata-strip tool into
    `<type>/<id>/`, and list it under `files`.
5.  Run `sync`; preview locally with `quarto preview` if wanted.
6.  Commit (the hook runs the checks) and push (CI deploys).

**Suggested order for the first launch (decided 2026-11-25).** Add every
public item as a row first (steps 1, 2, 5, 6 only), so the site launches
with complete lists. Then give items pages one at a time, adding a
summary, CC BY abstract or hosted file per item. Hosted files and rights
notes, the riskiest part, then come after the pipeline has run on real
data. This is the owner's habit, not a rule the code enforces.

### Decision updates this plan needs

Applied only after the design is approved:

*   **0004**: the license record moves to `data/abstract-licenses.yml`
    (above); `related` and `files` live in the authored file's front matter.
*   **0006**: generation is a separate step that reads only committed files;
    CI reruns it and compares. Pages are still committed.
*   **0009**: `build` also runs `generate --check`; the hook, not CI, is the
    privacy gate for what reaches GitHub; `sync` refuses to run without the
    hook.

### Risks and unverified points

*   Untested in Quarto 1.11.9: `render:` globs that skip `.md`; listing
    contents with external `path` values and `sort: false` (an external link
    in one list was tested, 0006); `-M` metadata on a website render; the
    sitemap's URL form (it may list `/<dir>/index.html` rather than
    `/<dir>/`; both reach the same file).
*   Byte-identical output on Windows and Linux is assumed, not tested.
    `.gitattributes` already forces LF.
*   Pattern scans catch formats, not meaning. A summary that names an
    unpublished study passes every check. Only the owner's reading stops
    it.
*   Google Scholar may ignore, or wrongly merge, a page that carries citation
    tags but not the full text. Not verified.
*   The pre-commit hook must be enabled once per clone
    (`git config core.hooksPath .githooks`); `sync` enforces it, but a commit
    made without running `sync` (a typo fix in `authored/`) relies on it
    being set.

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
*   **Reason for Rejection**: Rejected by author (2026-11-25): public text is
    written where it is published, and the vault stays private notes only.

### Alternative B: Owner-owned `index.qmd` with a Pandoc template

The owner writes `<type>/<id>/index.qmd`; `sync` writes a `_metadata.yml`
beside it; a Quarto title-block template draws the citation and meta tags.

*   **Pros**: the owner's text appears once in the repo; no generated copy.
*   **Cons**: citation formatting lives in Pandoc template syntax, which the
    owner does not maintain; depends on Quarto's metadata merging and partials
    staying the same across versions (untested); a page with only a hosted
    file still needs a generated `index.qmd`, so ownership ends up mixed.
*   **Reason for Rejection**: Rejected by author (2026-11-25): the same
    template-maintenance problem for which Hugo was rejected in 0006.

### Alternative C: Pages generated only in CI

Commit only data and authored text; CI generates the pages before
rendering, and they are never committed.

*   **Pros**: one step fewer when editing text (no `sync` rerun); a generated
    page cannot be edited by hand because none is in the repo; smallest
    diffs.
*   **Cons**: the owner never sees the published pages in a diff, only in a
    local preview; generation errors appear first in the GitHub log, a tool
    the owner does not use yet; reverses 0006's committed generated files.
*   **Reason for Rejection**: Rejected by author (2026-11-25): what is
    committed should be what is published, and errors should appear in the
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
*   **Reason for Rejection**: Rejected by author (0006): Quarto is maintainable
    in Python and R and can also make PDFs. The brief records the
    Python-renderer option as "not adopted" without a reason; the reason given
    here is the one that follows from 0006.

### Alternative E: Copy all vault fields, filter at render time

*   **Pros**: one copy step, no allowlist to keep in two places.
*   **Cons**: the repo's history would hold every private field once
    committed, and git cannot reliably forget.
*   **Reason for Rejection**: Rejected by author (0004): filtering happens on
    the vault side, before anything leaves it (0008), and again in `sync`.

### Alternative F: Privacy enforced only by the hookify rule

*   **Pros**: no extra code; already planned in CLAUDE.md.
*   **Cons**: it guards only Claude's actions on one machine; a commit made
    from a terminal or editor skips it.
*   **Reason for Rejection**: Rejected by author (0009): the checks run as a
    git pre-commit hook and again in CI; hookify is an extra layer for
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
    and BibTeX block to each page, which nobody asked for.
*   **Reason for Rejection**: chosen while drafting the Technical Plan,
    approved with it on 2026-11-25: `generate` writes the tags itself, so
    the format is known and the post-render check can verify it.

### Smaller choices already settled

| Alternative | Reason for rejection | Source |
| :--- | :--- | :--- |
| Bilingual from day one | Doubles writing and review for no current need. | 0001 |
| English under `/en/` | Longer links; moving English to the root later breaks them. | 0001 |
| Machine translation at build time | Sends text to an outside service; unreviewed output can misstate work. | 0001 |
| List pages with anchors only | Anchors are not permanent, citable addresses. | 0002 |
| Item pages for every type or item | Near-empty pages look worse than a row. | 0002 |
| Titles or dates in URLs | Titles change; preprint and published dates differ. | 0002 |
| `aliases:` instead of stable URLs | JavaScript-only redirects; clients without JavaScript see an empty page. | 0002 |
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
    one and the privacy scan needs no exemption for tests.

### Order of work

Each step is committed only when its tests pass. No generated data is
committed before steps 1 to 3 exist (CLAUDE.md, Pending setup).

0.  Quarto spike, outside the repo (below).
1.  `checks/` (pre-commit checks) and `.githooks/pre-commit`; enable the
    hook; local hookify rules.
2.  `sync/schemas.py`, `sync/files.py`.
3.  `.claude/settings.json` deny rule; `.gitignore`; CLAUDE.md rules.
4.  `sync/generate.py`, then `sync/importer.py`, then `sync/__main__.py`.
5.  `sync/abstract_license.py`, `sync/strip.py`.
6.  Quarto shells, `_quarto.yml`, `_includes/person.html`; the owner creates
    `authored/home.md` and `authored/research.md`.
7.  `checks/postrender.py`.
8.  `.github/workflows/build.yml`, `requirements.txt`; set the Pages source.
9.  `README.md`, `LICENSE`, `LICENSE-CONTENT.md`.
10. Decision updates (0004, 0006, 0009) and CLAUDE.md "Where things stand".
11. First real `sync` against the vault export; first push.

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
| 8 | Sitemap URL form; the marker text inside an `aliases:` redirect file. | Record what Quarto writes; the post-render check normalises `/x/index.html` to `/x/`. |
| 9 | Default theme loads nothing from another site. | Set `theme: none` plus a small local CSS file. |

Record the results in 0006 under "Tested" (step 10).

### Target Files to Create/Modify

#### 1. `checks/__init__.py` (Create)

*   **Type / Scope**: Python package marker.
*   **Proposed Changes**: Empty.

#### 2. `checks/privacy.py` (Create)

*   **Type / Scope**: Python module, used by the hook, CI and `sync`.
*   **Proposed Changes**: `scan_text(text, source_name, username=None) ->
    list[str]`.
    *   First removes the exempt patterns: DOIs (`10\.\d{4,9}/\S+`), the ORCID
        format (`\d{4}-\d{4}-\d{4}-\d{3}[\dX]`), ISO dates.
    *   Then looks for:
        *   absolute paths (`[A-Za-z]:[\\/]`, `/Users/`, `/home/`, `~/`);
        *   DNI (`\b\d{2}\.?\d{3}\.?\d{3}\b`);
        *   CUIL (`\b\d{2}-?\d{8}-?\d\b`);
        *   any email address (`[\w.+-]+@[\w-]+(\.[\w-]+)*\.[A-Za-z]{2,}`);
        *   phone numbers (`\+\d{1,3}[\s-]?\(?\d{1,4}\)?([\s-]?\d){6,}`,
            `\b(11|15)[\s-]?\d{4}[\s-]?\d{4}\b`);
        *   address words (case-insensitive `\b(calle|piso|depto|dpto)\b`);
        *   Argentine postal codes (`\b[A-Z]\d{4}[A-Z]{3}\b`).
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
    *   `old` is read with `git show <ref>:<path>`. If there is no ref (first
        commit, or CI with an all-zero `before`), the check is skipped and
        prints one line saying so.

#### 5. `checks/__main__.py` (Create)

*   **Type / Scope**: CLI, `python -m checks [--staged] [--base <ref>]`.
*   **Proposed Changes**: Gets the file list. With `--staged`, the list is
    `git diff --cached --name-only --diff-filter=ACMR` and the content comes
    from `git show :<path>`. Without it, the list is `git ls-files` and the
    content comes from disk. Then it runs:
    1.  The schemas from `sync/schemas.py` on `data/items.yml` (through
        `sync/export_schema.validate_export`), `data/manifest.yml`,
        `data/cv.yml`, `data/abstract-licenses.yml` and every
        `authored/**/*.md` front matter.
    2.  `privacy.scan_text` on every text file. The username is passed only
        with `--staged`, taken from `getpass.getuser()` and `Path.home()`.
    3.  `binaries.check_binary` on every other file.
    4.  The abstract-license rule: every authored `abstract` has a record
        whose `doi` equals the item's `doi` in `data/items.yml` and whose
        `url` matches `^https?://creativecommons\.org/licenses/by/`.
    5.  `append_only` against `HEAD` (hook) or `--base` (CI).
    6.  `sync.generate.check()`.

    It prints all errors, then exits 1 if there were any.

#### 6. `checks/postrender.py` (Create)

*   **Type / Scope**: CLI, `python -m checks.postrender _site`.
*   **Proposed Changes**:
    1.  Every line in `data/ledger.txt` maps to a file in `_site` (`/x/` →
        `x/index.html`). That file is a page, a tombstone (marker
        `data-tombstone` in the HTML) or an alias redirect (the marker found
        in Step 0).
    2.  Every `papers/*/index.html` that is not a tombstone has one
        `citation_title`, at least one `citation_author` and one
        `citation_publication_date`.
    3.  `sitemap.xml`, normalised, lists every built `index.html` except
        alias redirects.
    4.  `index.html` contains `Last updated \d{4}-\d{2}-\d{2}`.
    5.  No path under `_site` starts with `design/`, `docs/`, `data/`,
        `authored/`, `sync/` or `checks/`.
    6.  No `<script src>`, `<link href>` (stylesheet or font), CSS `@import`
        or `url()` in any built HTML or CSS points to another host.

#### 7. `checks/test_privacy.py`, `checks/test_binaries.py`, `checks/test_append_only.py`, `checks/test_postrender.py` (Create)

*   **Type / Scope**: Unit tests.
*   **Proposed Changes**:
    *   Privacy: each leak kind is caught; each exempt pattern (DOI, ORCID,
        date, `actions/checkout@v4`) is not; messages hold no matched text.
    *   Binaries: a PDF built in the test with an Author field fails, and the
        same PDF after `sync/strip.py` passes; a JPEG with EXIF fails; a
        6 MB file fails; a PDF whose text holds a fake email fails.
    *   Append-only: removal, reordering and a changed `id` fail; adding
        `withdrawn` passes.
    *   Postrender: run against a tiny `_site` tree built in a temporary
        directory, with one case for each failure.

#### 8. `.githooks/pre-commit` (Create)

*   **Type / Scope**: POSIX shell script (Git for Windows runs it with its
    own `sh`).
*   **Proposed Changes**: `exec python -m checks --staged`. It must be
    executable (`git update-index --chmod=+x`).

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
    keys).
    *   `validate_manifest`: a list of `{uid, type, id, withdrawn?}`. `type` is
        one of `papers`, `talks`, `posters`. The `id` regex is from the
        Technical Plan. `withdrawn` is a valid `YYYY-MM-DD`. `uid` and
        `(type, id)` are unique.
    *   `validate_authored`: front matter keys limited to `related` (list of
        `<type>/<id>`), `files` (list of entries with `path` xor `url`, plus
        `label` and `rights`, all non-empty strings; `path` has no `/` and
        no `..`) and `abstract` (string; papers only).
    *   `validate_cv`: `{date}`.
    *   `validate_abstract_licenses`: `{"papers/<id>": {url, doi, checked}}`.

#### 13. `sync/files.py` (Create)

*   **Type / Scope**: Python module.
*   **Proposed Changes**: `write_outputs(outputs, allowed)` as in
    Conventions. `read_front_matter(text) -> (dict, body)`, which splits a
    leading `---` YAML block.

#### 14. `sync/generate.py` (Create)

*   **Type / Scope**: Python module and CLI, `python -m sync.generate
    [--check]`.
*   **Proposed Changes**: `build_outputs(repo_root) -> dict[path, bytes]`,
    pure: it reads only committed files.

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
    out[data/ledger.txt] = sorted(ledger ∪ FIXED_PAGES ∪ item pages
                                  ∪ hosted file paths ∪ cv pdf if present)
    ```

    *   `FIXED_PAGES` = `/`, `/research/`, `/papers/`, `/talks/`,
        `/posters/`, `/cv/`.
    *   `derived_type`: `publication` → `papers`; `communication` with
        `format: poster` → `posters`; `oral` or `lecture` → `talks`.
    *   `related` targets must be in the manifest. Withdrawn targets are left
        out.
    *   Each hosted `files.path` must exist in `<type>/<id>/`.
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
        line), `resources` (hosted files), and `include-in-header` with the
        citation tags (papers only, as in the Technical Plan).
    *   **Item page body**, in this order: citation, status, links (DOI, free
        copy labelled by kind, preprint, `url`), summary, CC BY abstract with
        its label and license link, files with rights notes, related.
    *   **Tombstone:** title, `Withdrawn from this site on <date>.`, a
        `<div data-tombstone>`, nothing else.
    *   **CV page:** `[Curriculum vitae (PDF)](cv-public.pdf)`, `Updated
        <date>.` and `resources: [cv-public.pdf]`; or the placeholder line
        `The public CV will be posted here.`
    *   `main(check)`: build the outputs. With `--check`, compare them with
        the files on disk (staged content when called from the hook) and
        list every file that differs or is missing. Without it, call
        `write_outputs` with allowed patterns `*/listing.yml`,
        `papers|talks|posters/*/index.qmd`, `cv/index.qmd`, `data/ledger.txt`.

#### 15. `sync/importer.py` (Create)

*   **Type / Scope**: Python module.
*   **Proposed Changes**: `import_export(vault_dir, repo_root) ->
    (outputs, report)`.
    *   Load `<vault>/shared/cv/out/site-export.yaml` with
        `export_schema.load_export`.
    *   Keep records whose `uid` is in the manifest.
    *   For a manifest entry with `withdrawn`: if its `uid` is in the export,
        that is an error; otherwise keep its record from the current
        `data/items.yml`.
    *   For a manifest entry without `withdrawn` whose `uid` is absent: error.
    *   Sort by `date` descending, then `uid`; write `data/items.yml`.
    *   **CV:** if `<vault>/shared/cv/out/cv-public.pdf` exists, strip it
        with `strip.strip_pdf`, run `binaries.check_binary`, and compare with
        `cv/cv-public.pdf`. If different, output the PDF and a
        `data/cv.yml` with today's date. If the file is missing, output
        nothing for the CV.
    *   **Report:** counts of kept, withdrawn kept, not in manifest, and the
        CV state (`none`, `unchanged`, `updated`).

#### 16. `sync/__main__.py` (Create)

*   **Type / Scope**: CLI, `python -m sync [--dry-run]`.
*   **Proposed Changes**:
    1.  Fail unless `git config core.hooksPath` is `.githooks`.
    2.  Fail unless `VAULT_DIR` is set and points to an existing folder.
    3.  Run `importer`, then `generate.build_outputs` on the repo as it
        would be after the import (an overlay of the import outputs on
        disk).
    4.  Run `privacy.scan_text` on every text output and
        `binaries.check_binary` on the PDF. Any error stops the run before
        anything is written.
    5.  Print the report: rows, pages and tombstones per type; not in
        manifest; CV state.
    6.  Unless `--dry-run`, write the import outputs, then the generate
        outputs, each through `write_outputs` with its own allowed list
        (import: `data/items.yml`, `data/cv.yml`, `cv/cv-public.pdf`).

#### 17. `sync/abstract_license.py` (Create)

*   **Type / Scope**: CLI, `python -m sync.abstract_license papers/<id>`.
*   **Proposed Changes**:
    1.  Read the item's `doi` from `data/items.yml`, through the manifest.
    2.  `GET https://api.crossref.org/works/<doi>` with User-Agent
        `site-abstract-license-check/1.0`, no email, a 20-second timeout.
    3.  Accept the first `message.license[]` entry whose `content-version`
        is `vor` or `unspecified` and whose `URL` matches the CC BY pattern.
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
        `images/headshot.jpg` or `papers|talks|posters/<id>/<name>`. After
        stripping, it runs `binaries.check_binary`, then writes.

#### 19. `sync/test_generate.py`, `sync/test_importer.py`, `sync/test_schemas.py`, `sync/test_abstract_license.py`, `sync/test_strip.py` (Create)

*   **Type / Scope**: Unit tests. Fixtures are built in temporary
    directories from `design/site-export.sample.yaml`; no fixture `.qmd`
    files are committed.
*   **Proposed Changes**:
    *   Generate: a row-only item; an item with a summary gets a page and a
        ledger line; a CC BY abstract with and without a license record; a
        type mismatch error; a page in the ledger that lost its content
        errors; a withdrawn item with a page gets a tombstone; a withdrawn
        row-only item loses its row; `related` to a withdrawn item is left
        out; a preprint published in place keeps its URL and moves in order;
        running `build_outputs` twice gives identical bytes; `--check`
        reports a hand-edited page.
    *   Importer: every error row of the Lifecycle table; CV missing,
        unchanged and updated.
    *   Schemas: each rule accepts and rejects.
    *   Abstract license: saved Crossref replies for CC BY (`vor`), CC BY-NC,
        a `tdm` license only, and no license.
    *   Strip: output has no metadata and the same page count.

#### 20. `_quarto.yml` (Create)

*   **Type / Scope**: Quarto project config.
*   **Proposed Changes**:
    *   `project`: `type: website`, `output-dir: _site`, and `render:` set to
        exactly `index.qmd`, `research/index.qmd`, `cv/index.qmd`,
        `papers/**/*.qmd`, `talks/**/*.qmd`, `posters/**/*.qmd`. This is
        narrower than the Technical Plan's `**/*.qmd`, so no stray `.qmd`
        anywhere else can become a page.
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

*   **Type / Scope**: Owner file.
*   **Proposed Changes**: Created by Claude as `[]` with a header comment
    describing the entry format, before the deny rule goes in (step 3).
    From then on, only the owner edits it.

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
*   **Proposed Changes**: Triggers: push to any branch, and
    `workflow_dispatch`.
    *   **Job `check`:**
        1.  `actions/checkout` with `fetch-depth: 0`.
        2.  `actions/setup-python` with 3.13, then `pip install -r
            requirements.txt`.
        3.  `python -m unittest discover -t . -s sync` and the same for
            `checks`.
        4.  `python -m checks --base ${{ github.event.before }}`.
    *   **Job `build`** (needs `check`):
        1.  `quarto-dev/quarto-actions/setup` with `version: 1.11.9`.
        2.  `quarto render -M last-updated:$(git log -1 --format=%cs)`.
        3.  `python -m checks.postrender _site`.
        4.  `actions/upload-pages-artifact` with `path: _site`.
    *   **Job `deploy`** (needs `build`, runs only on `refs/heads/main`):
        `actions/deploy-pages`.

    Permissions are `contents: read`, `pages: write`, `id-token: write`, with
    one `pages` concurrency group. Each action is pinned to a release tag.
    Checks run on every branch so that the leak test (Verification) can
    exercise CI without deploying.

#### 30. `requirements.txt` (Create)

*   **Type / Scope**: Dependency pins.
*   **Proposed Changes**: `PyYAML==<x>`, `pypdf==<x>`, `Pillow==<x>`. Exact
    versions are chosen on the day of implementation and are also used
    locally.

#### 31. `.gitignore` (Modify)

*   **Type / Scope**: Git config.
*   **Proposed Changes**: Add `__pycache__/`, `.venv/` and
    `.claude/*.local.md` (the hookify rules, which contain the username).

#### 32. `.claude/settings.json` (Modify)

*   **Type / Scope**: Claude Code project settings (tracked).
*   **Proposed Changes**: Add `permissions.deny`: `Edit(authored/**)`,
    `Write(authored/**)`, `Edit(data/manifest.yml)`,
    `Write(data/manifest.yml)`. No machine-specific paths.

#### 33. `.claude/hookify.owner-files.local.md`, `.claude/hookify.private-data.local.md` (Create, local, untracked)

*   **Type / Scope**: Hookify rules (CLAUDE.md Pending setup).
*   **Proposed Changes**:
    *   The first rule blocks any Bash command that writes to `authored/` or
        `data/manifest.yml` (redirections, `sed -i`, `cp`, `mv`, `tee`,
        `rm`).
    *   The second rule blocks `git commit` when the staged diff matches the
        privacy patterns or the username, as a Claude-side duplicate of the
        hook.
    *   Both rules are created with the hookify plugin's own commands, not by
        hand.

#### 34. `CLAUDE.md` (Modify)

*   **Type / Scope**: Project instructions.
*   **Proposed Changes**:
    *   Add to Rules: "Never write `authored/**` or `data/manifest.yml`;
        propose text in chat." and "Run `python -m sync`; never edit
        generated files."
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
    *   the commands `sync`, `sync --dry-run`, `sync.abstract_license`,
        `sync.strip`, `quarto preview`, the tests;
    *   the six "Adding an item" steps;
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

#### 39. `docs/decisions/0004-data-schema.md`, `0006-site-generator.md`, `0009-privacy-and-permanence.md` (Modify)

*   **Type / Scope**: Decision records, updated after the design is
    approved.
*   **Proposed Changes**:
    *   0004: the license record moves to `data/abstract-licenses.yml`;
        `related` and `files` live in the authored front matter.
    *   0006: the two-step `sync`; CI reruns `generate --check`; the Step 0
        results under "Tested".
    *   0009: `build` runs `generate --check`; the hook is the privacy gate
        for what reaches GitHub; `sync` refuses to run without the hook.

    Each change is dated 2026-11-25 or later.

#### 40. `images/headshot.jpg`, hosted item files (Create, when the owner provides them)

*   **Type / Scope**: Owner-provided binaries.
*   **Proposed Changes**: These are always added through `python -m
    sync.strip staging/<file> <dest>`, and only when the owner names the
    file (0004).

### Verification Plan

*   **Compilation/Build**: `quarto render` (local and CI, Quarto 1.11.9).
*   **Unit Tests**: `python -m unittest discover -t . -s sync` and
    `python -m unittest discover -t . -s checks`, run locally and in CI.
*   **Static Analysis & Linting**: none added (no unrequested
    dependencies); `python -m checks` is the repo's own static check.
*   **Test Coverage Requirement**: every row of the Lifecycle table and
    every check in `checks/` has at least one passing and one failing test.
    No percentage target, since that would need a coverage tool.
*   **E2E/Integration**:
    1.  **Fake vault.** Copy `design/site-export.sample.yaml` into a scratch
        folder as `shared/cv/out/site-export.yaml` and set `VAULT_DIR` to
        it. Add manifest entries for the five sample uids in a scratch
        clone (never committed). Run `sync`, `quarto render` and
        `checks.postrender`, and confirm rows, pages, a tombstone and the
        sitemap.
    2.  **Hook leak test.** In a scratch clone, stage one file per leak kind
        (fake values) and a PDF with metadata. Each commit is refused.
    3.  **CI leak test.** Only with the owner's approval at that time: a
        `leak-test` branch with one fake leak, committed with `--no-verify`
        by the owner. The `check` job fails and nothing deploys. The branch
        is then deleted.
    4.  **Ledger test.** In a scratch clone, delete a generated page for a
        ledger URL. `generate --check` and `checks.postrender` both fail.
    5.  **Fresh clone.** The first push to `main` builds and deploys from a
        clean checkout (the Zero cost, no lock-in goal).
    6.  **Timed walkthrough.** Add the first real item following "Adding an
        item" and record the minutes (the 10-minute goal).

--------------------------------------------------------------------------------

*Drafted with EGM*
