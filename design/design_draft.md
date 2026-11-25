# Academic website

*   **Author:** Abraham Yeffal
*   **Status:** Draft
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
3. **Links must not break.** GitHub Pages cannot redirect, and academics
   paste links to single items into CVs, forms and papers. A URL that moves
   or disappears breaks every saved copy.

The proposed solution: the vault side exports only what the owner has
approved; this repo copies only allowlisted fields from that export, checks
every commit and every build for private data, and keeps a ledger so that no
released URL can vanish.

## Goals

Each goal states how it will be checked.

*   **Findable.** Every paper page carries citation meta tags; the site has a
    sitemap listing every page; the home page links ORCID
    `0000-0002-9645-6664` and the one Google Scholar profile (0009, 0010).
    Check: the build fails if a paper page lacks the tags or a page is missing
    from the sitemap.
*   **One source of truth.** Every paper, talk and poster shown on the site
    comes from the vault export. This repo adds only the owner's authored
    text (or a CC BY paper's abstract), the `id`, `related` links and `files`
    entries (0004). Check: `sync` is the only program that writes item data,
    and it reads only the export and the public CV PDF.
*   **Private by construction.** No commit and no deploy goes through if the
    committed data holds a key not on the allowlist, an absolute path, a
    username or a DNI/CUIL pattern. The same checks run before each commit and
    again in the automatic build (0009). Committed PDFs and images (the CV,
    hosted files, the headshot) have their metadata stripped (0004, 0008,
    0010). Check: a test commit with each kind of leak, including a file with
    metadata, is refused by both.
*   **Permanent URLs.** Any link to an item or page that has ever been
    shared keeps reaching that item or page. GitHub Pages cannot redirect,
    so URLs are chosen with foresight to never need changing, and an ID is
    never reused for a different item (0002). Check: the build fails if any
    URL in the committed ledger (the list of every URL ever published) has
    none of: a page, a tombstone (a page left at the URL saying the item was
    withdrawn), or a Quarto `aliases:` redirect to the page's new address,
    used only as a safety net when a page has to move.
*   **Zero cost, no lock-in.** The site builds from a fresh clone with pinned
    Quarto (tested with 1.11.9) and Python, and uses no paid service (0006).
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

--------------------------------------------------------------------------------

*Drafted with EGM*
