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
when it has a summary written by the owner or a hosted file. Otherwise it is
a row on its list page that links to the publisher or to a public page (0002).
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
    text, the `id`, `related` links and `files` entries (0004). Check: `sync`
    is the only program that writes item data, and it reads only the export.
*   **Private by construction.** No commit and no deploy goes through if the
    committed data holds a key not on the allowlist, an absolute path, a
    username or a DNI/CUIL pattern. The same checks run before each commit and
    again in the automatic build (0009). Check: a test commit with each kind
    of leak is refused by both.
*   **Permanent URLs.** A released URL is never removed, renamed or reused
    (0002). Check: the build fails if any URL in the committed ledger has no
    page or tombstone.
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
    (0008). This design only reads the export and, where decided, hosts the
    public CV PDF.
*   The individual CV and its contact details. They never enter this repo
    (0008).
*   Reading the vault from this repo, at any time (CLAUDE.md, 0008).

## Open Questions

*   **Vault agent: path for the public CV PDF (0008).** The design has `sync`
    copy the public CV from a second fixed path next to the export. The vault
    agent has not agreed to it or named the path yet. Request drafted, not yet sent:
    `design/request-3-to-vault-agent.md`.
*   **Quarto `aliases:`** may provide client-side redirects, which would
    soften the "no redirects" premise of 0002. Not verified.
*   **Co-author removal procedure.** Co-author names are third-party data. No
    procedure for a removal request is written.
*   **Authored summaries that paraphrase a publisher abstract** might carry
    third-party rights, and CC BY 4.0 cannot be withdrawn (0004, 0007). No
    checking rule is written.
*   **Larger files.** Zenodo remains an option for files over the 5 MB cap
    (0009). Not decided.
*   **Photo on the home page** (0010). No decision.

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
    its metadata and scans its text before writing it (0008). The path still
    needs the vault agent's agreement.
*   **Search Console.** Register with Google Search Console and import into
    Bing Webmaster Tools, once the site is live (0010).

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
