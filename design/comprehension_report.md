# Stage 6: Comprehension Test Report

- Target: `design/academic-website.md` at commit `55211d0`
  - FeatureRange: lines 1–764
  - DetailedRange: lines 765–1458
- Date: 2026-11-26
- Reviewer: Comprehension, in a fresh context. No document standard applies to this stage.
- Goldfish context:
  - `design/concepts_brief.md`
  - `docs/decisions/0001`–`0010`
  - `design/site-export.sample.yaml`
  - `sync/export_schema.py`
  - `sync/test_export_schema.py`
- What the reviewer read: the context files, except decisions 0001, 0005 and 0006 and `test_export_schema.py`. The feature range cites those only for points it already explains.

## What this proposes

The design is a five-page static academic site (Home, Research, Papers, Talks and posters, CV), built with Quarto and hosted on GitHub Pages. Its item data comes from an export file that a separate private vault-side repo writes. A local `sync` program runs in two steps:

- **import** checks the export and keeps only the records whose `uid` the owner has listed in a committed, append-only manifest. It also copies a public CV PDF after scanning it and stripping its metadata.
- **generate** reads only committed files: data, the owner's text in `authored/`, and the ledger. From them it writes:
  - the list pages, item pages and tombstones;
  - the CV page;
  - an append-only ledger of page URLs.

An item gets its own page only if it has owner text, a hosted file or a CC BY abstract. Otherwise it is just a row on its list page.

The same privacy checks run in the pre-commit hook, in the pre-push hook and in CI: allowlist schemas, pattern scans, metadata checks on binary files, append-only checks and `generate --check`. CI then renders the site, runs the post-render checks and deploys. The post-render checks cover four things: every ledger URL exists, the citation tags, the sitemap, and nothing loaded from other sites.

The local hooks are the real privacy gate, because a pushed commit is already public. CC BY abstracts and hosted item files are deferred to "Phase 2".

## How the existing system works, per this document

Nothing is built yet except `sync/export_schema.py`. It validates the export against schema version 1 and rejects unknown keys.

The vault side already writes `shared/cv/out/site-export.yaml`, and the real export is currently `items: []`. It holds only the items the owner has marked public, and only allowlisted fields. No CV builder exists yet, so there is no CV PDF.

Decisions 0001 to 0010 are the governing record, and the design proposes amendments to 0002, 0004, 0006 and 0009. The older concepts brief is superseded wherever it conflicts with them.

## Findings

**Verdict:** no Blockers. The reviewer could paraphrase every section of the feature range, and the sections on data flow, ownership and checks connect. There are 3 Majors and 11 Nits.

| # | Sev. | Location | Finding | Suggested direction |
| :--- | :--- | :--- | :--- | :--- |
| C1 | 🟡 Major | Lifecycle row "CV PDF unchanged" (466); Risks (622–623) | "Step 0 #10" and `strip_pdf` are used in the feature range but are defined only in the detailed range (833, 849). A reader of the feature range can't tell how a CV change is decided. | One sentence: a throwaway test runs before building. If stripping doesn't give the same bytes every run, "changed" is decided by a hash of the source PDF kept in `data/cv.yml`. |
| C2 | 🟡 Major | Goals, "Credible" (68–72) | The goal says the site and the CV list the same items. But the site also needs a manifest entry, which the CV doesn't, so the site can list fewer. The only sign of that gap is the "not in manifest" count, and the stated check (the last-updated date) doesn't test it. | Restate the goal: same eligibility rule, and any gap shows as a non-zero "not in manifest" count. Or name a check that enforces it. |
| C3 | 🟡 Major | Settled "Withdrawal" (138–140); Lifecycle (460–461) | Withdrawal has no step-by-step workflow. The rule that consent must first be removed in the vault and the export re-run appears only in 0009, so following this document alone leads to an error. | Add a "Withdrawing an item" list next to "Adding an item": remove consent in the vault, export, add `withdrawn`, `sync`, delete hosted files, commit. |
| C4 | 🟢 Nit | Authored front matter (375–391); Adding an item (571–573) | The `abstract` and `files[].path` keys appear as if they work now. Phase 2 is defined only in passing (203–204). | Define Phase 2 in the Technical Plan and mark the two keys "(Phase 2; rejected until then)". |
| C5 | 🟢 Nit | Type rule (421), display rules | Export fields are never introduced: `type`, `format`, `date_precision`, `pub_status`, `open_copy_kind` and `abstract_published_in`. | One sentence pointing to `site-export.sample.yaml` and 0004. |
| C6 | 🟢 Nit | Adding an item, step 2 (569) | It says to copy the `uid` "from the vault note", but not where on the note. The `sync` report shows counts only, so it can't say which `uid` is missing. | State where the `uid` is read: the note's front matter or the export file. |
| C7 | 🟢 Nit | 181, 185–189, 207, 247, 327, 342–344, 703–710 | Terms used without definition: "vault agent", "reply 1/3", "registry notes", "ZotLit", "hookify", "Claude" as an actor, `CLAUDE.local.md`. | A short glossary, or an explanation beside each term. |
| C8 | 🟢 Nit | Repo layout (293, 300); Who writes what (331); Lifecycle (461–462) | The layout calls hosted files "owner-added", the table says the strip tool writes them, and the owner deletes them. This breaks "No file is both". | Say "written by the strip tool, run by the owner; the owner may delete them". |
| C9 | 🟢 Nit | "One source of truth" check (76–77) | "`sync` reads only the export and the CV PDF" is too narrow. It also reads the manifest, `items.yml`, the authored files and the ledger. | Say it "reads nothing else from the vault". |
| C10 | 🟢 Nit | Lifecycle (454) | "The export counts it as 'not in manifest'" is wrong: it is `sync`'s report that counts it. | Fix the subject. |
| C11 | 🟢 Nit | Ledger definition (93, 305) | A URL enters the ledger when its page is generated and committed, before any push. So a page that was committed but never pushed is still permanent. | Define the ledger as "every page URL ever generated and committed", or state that consequence. |
| C12 | 🟢 Nit | Status line (4–5) | It still says "Not yet reviewed with `/egm:egm-review`". | Update it. |
| C13 | 🟢 Nit | 94, 535, 598 | Bare dates such as "(2026-11-26)" read like citations that point nowhere. | Say once that a bare date marks a choice made in this design, to be written into the decisions listed for step 10. |
| C14 | 🟢 Nit | 80, 490 | DNI and CUIL are not explained. | Gloss them: Argentine national ID number and tax/labour ID number. |

## Notes from the orchestrator

- **C2 is a real gap, not just wording.** The manifest gate means the site and the CV can disagree for as long as an item sits in the export without a manifest entry. The design already reports that count, so the cheapest fix is the restatement suggested above.
- **C11 is minor.** An unpushed commit can still be dropped with `git reset`, which also reverts the ledger. In practice a page becomes permanent once it is pushed, but the document should say so.
