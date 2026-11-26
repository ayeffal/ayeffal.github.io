# Stage 5: Initial Zoom Out Report

- Target: `design/academic-website.md` (whole file, lines 1–1342)
- Date: 2026-11-26
- Reviewers: Zoom Out and Inventive Catalyst, run in parallel, each in a fresh context.
- Goldfish context:
  - `design/concepts_brief.md`
  - `docs/decisions/0001`–`0010`
  - `design/site-export.sample.yaml`
  - `sync/export_schema.py`
  - `sync/test_export_schema.py`

## Summary

Neither reviewer found a Blocker. Between them they raised 8 Majors and 13 Nits. Four topics came up in both reports, and each counts once in the action list below:

1. **`generate`'s input interface** (ZO M3, IC 4). The hook compares staged outputs with outputs regenerated from the working tree, so a commit with only some files staged can pass or fail when it shouldn't. Both reviewers suggest passing `build_outputs(read)` a reader function.
2. **The CV "unchanged" check** (ZO N4, IC 3). pypdf probably writes a new trailer `/ID` each time, so comparing stripped bytes reports a change on every `sync`. Compare a hash of the source PDF, or of its content, instead, and test that in Step 0.
3. **Internal contradictions** (ZO N3, IC consistency):
   - Python 3.12 or 3.13;
   - which branches the CI trigger runs on;
   - the `render:` list.
4. **Permanence versus removal** (ZO M2, IC 2, IC 6). The permanence rules block operations the design itself promises: removing a hosted file and moving a page. Withdrawn records also keep their full data forever.

## Consolidated action list

| # | Sev. | Finding | Source |
| :--- | :--- | :--- | :--- |
| A1 | 🟡 Major | The privacy scan matches the repo's own files: the design doc, `checks/privacy.py` and the decisions. Step 1 would be refused by its own hook, and `actions/checkout@v4` matches the email pattern but isn't in the exempt list. Decide the scan scope, or keep an explicit list of exempt paths. | ZO M1 |
| A2 | 🟡 Major | Hosted files are in the ledger, but a tombstone is an HTML page at `/x/`. So taking down a co-owned file, or withdrawing an item that has a file, fails the build. Pick a rule; the reviewer prefers taking file paths out of the ledger. | ZO M2 |
| A3 | 🟡 Major | The `aliases:` safety net for moved pages has no input path. The manifest is append-only and `uid` must be unique. Generated pages are tool files, and no data format carries an alias. Proposal: allow an appended move record in the manifest. | IC 2 |
| A4 | 🟡 Major | Define the input interface of `build_outputs` (disk, index or overlay) at the architecture level. | ZO M3, IC 4 |
| A5 | 🟡 Major | The privacy guarantee rests on a client-side hook that `--no-verify` skips, and E2E 3 pushes a fake leak to the public repo. Options, heaviest first: a private source repo whose CI deploys to the public repo; or a `pre-push` hook that checks the whole push range. | IC 1 |
| A6 | 🟡 Major | Optional features are built before any item needs them: the Crossref abstract-license tool, its data file and schema, check 4, the hosted-file strip CLI, and building all three types at once. Move them to a Phase 2, matching the launch order. | ZO M4 |
| A7 | 🟡 Major | The reasons for Quarto are out of date. Python now writes the bodies, rows, citation tags and tombstones, and the "Quarto can also make PDFs" advantage lapsed with 0008. Restate why Quarto stays, or keep "Python writes the HTML" as a real fallback. Smaller option: generate the list pages as Markdown tables, which drops `listing.yml` and Step 0 items 2–3. | ZO M5 |
| A8 | 🟡 Major / 🟢 Nit | The CV "unchanged" check probably fails every time. Decide by a hash of the source or of the content, and add a Step 0 row for it. | IC 3, ZO N4 |
| A9 | 🟢 Nit | The CI append-only baseline `github.event.before` breaks after an approved history rewrite or on a new branch. Option: publish the ledger and use the live copy as the baseline. | IC 5 |
| A10 | 🟢 Nit | A withdrawn item's full record stays in `items.yml` forever. Option: cut it down to `uid`, title and date in a separate `tombstones.yml`. | IC 6 |
| A11 | 🟢 Nit | Fix the contradictions: Python 3.12/3.13 (lines 527, 723, 1193); CI on `main` or on any branch (lines 220, 526, 1189); `render:` glob or explicit list (lines 300, 511, 1092–1096). | ZO N3, IC |
| A12 | 🟢 Nit | The hookify rule duplicates the regexes in `checks/privacy.py`. Make it block `--no-verify`, changes to `core.hooksPath` and edits to `.githooks/` instead. | ZO N1 |
| A13 | 🟢 Nit | `sync` and `checks` import each other. Pick one direction. | ZO N2 |
| A14 | 🟢 Nit | Implementation detail in the Technical Plan: the `id` regex (line 347), the pattern lists (464–469) and the pseudocode (943–963). | ZO N5 |
| A15 | 🟢 Nit | `sync/schemas.py` should import `_valid_date` and `UID_RE` from `export_schema.py` instead of redefining them. | ZO N6 |
| A16 | 🟢 Nit | Leftovers: `authored/<type>/<id>.es.md` (line 284) is out of scope. Search Console verification (line 143) has no file or meta-tag step. | ZO N7 |

## What the reviewers found sound

- **Inventive Catalyst** checked these and found no false compromise:
  - committed generated pages, kept honest by `generate --check`;
  - tombstones plus the ledger;
  - the two-stage allowlist;
  - generating locally and checking in CI;
  - the split between owner files and tool files;
  - citation tags written in Python.
- **Zoom Out:** the architecture serves the root problem (a private vault and permanent URLs), and the context is enough to judge it.

## Reviewer reports, verbatim

### Zoom Out

**Context sufficiency:** passes. **Verdict:** no Blockers, 5 Majors, 7 Nits.

- **M1, the privacy scan fails on the repo's own files.** See lines 464–472, 790–807 and 843.
  - The scan covers every tracked text file. The design doc (line 465) and `checks/privacy.py` contain the path patterns it looks for. The hook refuses the commit at step 1.
  - The tests expect `actions/checkout@v4` to be exempt (line 878), but it isn't in the exempt list (lines 793–794).
  - Direction: scan only data/, authored/, the generated outputs, the text of binaries and the shells. Or keep an explicit list of exempt paths. Add `@v<digits>` to the exempt list.
- **M2, hosted files are in the ledger, but nothing lets one be removed.** See lines 148–151, 387–390, 440, 443, 487–489 and 858–861.
  - A tombstone is HTML at `/x/`, so a ledger line for a PDF can never be satisfied.
  - The Lifecycle table has no "hosted file removed" row.
  - Direction: (a) take hosted-file paths out of the ledger (the reviewer's choice); or (b) serve an HTML notice at the file's path, which is weak.
- **M3, `generate` has three callers that read inputs differently.** See lines 262–266, 940, 992–994, 1025–1027 and 850.
  - The callers read from the working tree, from the git index and from an in-memory overlay.
  - Direction: `build_outputs(read)`, where `read(path) -> bytes | None`.
- **M4, optional features are built before anything needs them.** See lines 376–382, 1037–1053, 289, 927, 477, 1055–1065, 192–193 and 545–550.
  - The brief records 2 publications and 11 communications, none with a summary or a hosted file.
  - Direction: order the work to match the launch, and record the optional parts as Phase 2. A minimal `strip_image` for the headshot comes first.
- **M5, the reasons for Quarto no longer match the architecture.** See lines 634–648, 392–399, 415–422, 762–777 and 564–570.
  - The PDF and CV argument lapsed with 0008. The costs remain: about 476 MB, version pinning and 9 unverified behaviours.
  - Direction: restate the reasons, or treat "Python writes HTML plus a sitemap" as a fallback. Optionally, make the list pages Markdown tables.
- **N1:** the hookify regex rule duplicates the hook. Make it block `--no-verify`, `core.hooksPath` and edits to `.githooks/` instead.
- **N2:** `sync` and `checks` import each other. Pick one direction.
- **N3:** contradictions on the Python version, the `render:` list and the CI trigger.
- **N4:** CV bytes change on every write (the pypdf `/ID`). Compare a content digest.
- **N5:** the Technical Plan includes regexes and pseudocode.
- **N6:** reuse `_valid_date` and `UID_RE` from `export_schema.py`.
- **N7:** the `.es.md` layout line and Search Console verification are left over.

### Inventive Catalyst

**Verdict:** the foundation is mostly balanced. Two Majors, one Major still to verify, three Nits, and one consistency Nit.

1. **Major: the guarantee rests on a client-side hook.** See lines 502–506, 578–581, 1329–1332 and 78–86.
   - Resolution, Intermediary / Extraction: keep the source in a private repo, and let its CI push the build to the public repo with a deploy key.
   - Lighter option: a `pre-push` hook that runs `checks` over `@{u}..HEAD`.
   - Costs: two repos to keep in step, a deploy-key secret, a public repo without its source, and Actions minutes, which are capped for private repos. Decisions 0006 and 0009 would need amending.
2. **Major: aliases have no input path.** See lines 403–406, 87–94, 346–349 and 308–315.
   - Resolution, Inversion: treat the manifest as an append-only event log that allows move records. `generate` then writes `aliases:` from them.
   - Costs: a more complex manifest schema, resolving which entry is active for a `uid`, and an update to 0002 or 0009.
3. **Major (to confirm in Step 0): the CV "unchanged" check compares stripped bytes.** See lines 1011–1015, 447 and 384–385.
   - Resolution, Preliminary Action: add a `source_sha256` field to `data/cv.yml`, and add a Step 0 row for strip determinism.
4. **Nit: `build_outputs` reads disk in the hook.** See lines 992–994, 938–941 and 835–838.
   - Resolution: pass in a reader; the hook uses `git show :path`.
5. **Nit: the `github.event.before` baseline breaks after a history rewrite or on a new branch.** See lines 480–481, 828–830 and 1197.
   - Resolution: publish `/ledger.txt` and compare with the live copy.
6. **Nit: withdrawn records keep all their data.** See lines 351–355, 1006–1008 and 148–151.
   - Resolution, Segmentation: move a minimal record into `data/tombstones.yml`.

**Consistency:** Python 3.12 or 3.13 (lines 527, 723, 1193); CI on `main` or on any branch (lines 220, 526, 1189).

**No false compromise found** in the owner/tool file split, generating locally plus CI checks, the two-stage allowlist, tombstones plus the ledger, or citation tags in Python.
