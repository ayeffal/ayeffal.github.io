# Stage 7: Critic Review Report

- Target: `design/academic-website.md` at commit `08ca38b`, FeatureRange lines 1–838
- Date: 2026-11-27
- Reviewers: egm-design and egm-structural, both against `feature-spec-standard`, plus egm-style. Each ran in a fresh context, and all three completed.
- Goldfish context:
  - `design/concepts_brief.md`
  - `docs/decisions/0001`–`0010`
  - `design/site-export.sample.yaml`
  - `sync/export_schema.py`
  - `sync/test_export_schema.py`
  - The style reviewer got only the brief and the decisions.

## Summary

No reviewer found a Blocker. Together they raised 19 Majors and 29 Nits, which merge into the 14 Majors and 12 Nits below.

Two themes stand out:

1. **The C2 change (2026-11-27) hasn't caught up with the rest of the document.** `sync` now proposes IDs and writes the manifest, but:
   - the decision-update list leaves out 0003, and 0009 is listed without these changes;
   - a withdrawal can now be triggered by mistake;
   - the interactive-terminal check is treated as a control.
2. **The goals claim more than their checks test:**
   - Credible: the site and the CV list the same items;
   - Private by construction;
   - Permanent URLs for "any page".

The structural reviewer also found that the standard's "Risks" requirement is met only by a sub-heading, and that the Open Questions section holds settled design.

## Consolidated findings

| # | Sev. | Lines | Finding | Direction | Source |
| :--- | :--- | :--- | :--- | :--- | :--- |
| K1 | 🟡 Major | 9–11, 658–675 | "Decision updates this plan needs" is incomplete. It leaves out 0003: the ID tag is no longer typed by hand, and the year is now the year of `date`. The 0009 entry is missing: `sync` now adds `withdrawn` and refuses to finish while an exported item has no ID (0009 says it "reports the rest as counts"). The 0004 visibility gates and 0007 (the license moves out of the authored file) are missing too. Step 10 (line 889) lists 0003, so the two lists disagree. Line 11 points to step 10, which is outside the range. | Add the entries; point line 11 at the in-range heading. | design M1, structural M3, style M5 |
| K2 | 🟡 Major | 90–96, 175–177 | The Credible goal overclaims. "The site cannot lag behind the CV" is true only right after a `sync`. The CV PDF is built separately, and nothing confirms the CV builder uses the same site-consent filter as the export. The check compares the export with the manifest, not the CV with the site. | Reword: "after each `sync`, every exported item is on the site". Separately, confirm with the vault side whether the CV uses the export's item set. | style M1, design M8, structural N6 |
| K3 | 🟡 Major | 404–410, 503–508, 637–644 | A withdrawal can be triggered by mistake and can't be undone. An empty or partial export (`items: []` is valid) offers to withdraw every item. The default answer to the withdraw prompt isn't stated, and the ID prompt teaches the owner to press Enter. Once pushed, `withdrawn` can't be removed and the `uid` can't get a new ID, so the item can never come back. | Default to "no" and require typing `withdraw`. Refuse when the export is empty, or when more than a couple of items vanish at once, unless an override flag is given. State that there is no recovery, or design one. | design M2 |
| K4 | 🟡 Major | 385–388, 503 | The terminal check is treated as a guard. Anything that fakes a terminal gets past it (`script`, `winpty`, Python's `pty`). The opposite can also happen: under Git Bash (mintty), a native Windows Python may see no terminal and refuse the owner's own run. That is untested. | Call it a convenience, not a control. Add a Step 0 test: the prompt works in the owner's real shells. Optionally add a hookify rule against piping answers into `sync`. | design M4 |
| K5 | 🟡 Major | 103–112, 551–554 | "Private by construction" overclaims: "no commit and no deploy goes through" and "the same checks run" in CI. The hooks can be skipped, and the username check is local only. The binary check covers only the Info dictionary and XMP. A PDF also has embedded-image EXIF, annotations and attachments, and an image-only PDF passes the text scan with nothing to scan. Commit author emails are public and nothing checks them against the contact address (0008). | Calibrate the goal. Add a hook check on the commit author and committer email. Phase 2: the strip tool re-encodes images and drops annotations and attachments; a PDF with images but no text needs the owner's confirmation. | style M2, design M6, M9 |
| K6 | 🟡 Major | 536–547 | Tracked files outside the scan scope can carry absolute paths and usernames: `.claude/settings.json`, `CLAUDE.md`, `.githooks/`, `.gitignore`, `requirements.txt`. | Run the path and username patterns on every tracked file. Limit only the vault-data patterns to the published scope. | design M5 |
| K7 | 🟡 Major | 542–550 | The scan patterns aren't pinned against the data's normal shapes. Old Argentine postal codes are four digits, so they collide with years, page ranges, volumes and article numbers. Phone patterns collide with page ranges. | Pin each pattern (CPA form only; phones with `+54` or separators). Test every pattern against the sample export and the generated pages. | design M7 |
| K8 | 🟡 Major | 558–560, 579–590 | Removing a leak by rewriting history (allowed by 0009) fails the append-only check in CI, so the leaked page stays live. The baseline for a manual run, the first push and a force push is undefined. This extends Stage 5 A9, which was skipped as a known gap; the leak-removal case makes it more serious. | Define an owner-approved leak-removal path. State CI's baseline in each case. | design M3 |
| K9 | 🟡 Major | 113–121, 345, 454–455, 632–633 | The Permanent URLs goal is wider than its check. "Any page" includes the hand-written shells, but the ledger holds only what `generate` produces. When a URL becomes permanent is described four ways: shared, committed, produced and pushed. | Narrow the goal to what the check covers, and use "pushed" everywhere. State whether the shell pages go in the ledger. | style M3, design N3 |
| K10 | 🟡 Major | 211–213 vs 506 | "A missing summary is never an error" contradicts the Lifecycle row: emptying a page that is in the ledger is an error. | "A summary never written is never an error; removing the only content of a pushed page is." | style M4 |
| K11 | 🟡 Major | 579–590, 677–697 | The standard asks for risks with mitigations. They sit under a sub-heading, and the main exposure risk is under Checks. These have no mitigation: Scholar ignoring pages, the untested Quarto behaviours (the fallback is only in Alternative D), and scans that catch formats, not meaning. Scalability is missing: PDFs accumulating in git history, Pages size limits. | Add an H2 Risks & Mitigations with one row per risk, and move "What the hooks cannot do" into it. | structural M1 |
| K12 | 🟡 Major | 149–246 | "Open Questions: None remaining" is followed by about 100 lines of settled design. Some of it appears nowhere else: the ID-suggestion rule, list order, the CV path, Search Console, the co-author removal steps, the photo rule. Line 155 says these "go into the Technical Plan", but they haven't been moved. | Move the settled items into the Technical Plan (the ID rule goes next to the manifest format) and leave Open Questions empty. | structural M2 |
| K13 | 🟡 Major | 718–782 | Alternatives say "Rejected by author" with a date or a bare decision number and no link. The standard forbids attributing a rejection without a linked record. The new C2 choice (sync suggests IDs, versus a hand-edited manifest) has no Alternatives entry. | Reword each as "Rejected: <reason>" and link the decision files. Add the C2 alternative. | structural M4, design N7 |
| K14 | 🟡 Major | 176–179 | An uncited "common academic-site practice" is used as a design reason. The orchestrator added it on 2026-11-27. | Drop the clause; the vault consent (0009) is the real reason. | style M6 |
| K15 | 🟢 Nit | 167–176 | Gaps in the ID-suggestion rule: compound surnames and particles; title words with digits or Greek letters (`2D`, `fMRI`, `α-synuclein`), which the regex rejects; what happens when both tag words are taken; no "skip/quit" answer when the shown type is wrong. The 0003 year is now read as the year of `date`, which should be said explicitly. | Write the cases down and add skip/quit. | design N1, N2 |
| K16 | 🟢 Nit | 3–12, 153, 250 | Metadata and dates. The Status line reads like a changelog and says "Approved 2026-11-25" although the C2 change is dated 2026-11-27. The reading note sits between Status and Date. "Settled during drafting (2026-11-24)" holds items from 11-26 and 11-27, and the 11-25 section comes after it. | One status line that records the re-approval, and fix the heading dates. | all three |
| K17 | 🟢 Nit | 43–55, 268–276 | There are two glossaries. "Manifest" is never defined. "Ledger" and "Phase 2" are used before they are defined. "Step 0" resolves only outside the range. | Merge into one Terms list near the top and add the manifest. | structural N2, style N7 |
| K18 | 🟢 Nit | 280–311 | The data-flow diagram leaves out the withdrawal prompt. | Add it. | structural N9 |
| K19 | 🟢 Nit | 115, 319, 489, 581, 655, 803 | Filler and idiom: "with foresight", "like with like", "nobody asked for", "the real privacy gate", "the riskiest part". | Cut or calibrate. | style N3 |
| K20 | 🟢 Nit | 123, 320, 386–388, 618 | Some wording is stronger than the evidence: "pinned … pinned"; "cannot give a false result"; "cannot add an ID"; "(the 10-minute path)", although the goal is not yet shown. | Calibrate. | style N4–N6 |
| K21 | 🟢 Nit | 26, 108, 211, 270, 672 | The deploy stage has four names: build, automatic build, `build`, CI. | One name. | style N8 |
| K22 | 🟢 Nit | 113–121 | In the Permanent URLs goal, new rules come after "Check:". | Put them before it. | structural N5, style N9 |
| K23 | 🟢 Nit | 72, 115, 123, 359, 524, 610; 66; 516–525 | Formatting: long unwrapped lines, a list marker with one space, and the hooksPath sentence tacked onto the end of the prompt paragraph. | Rewrap; split the paragraph. | structural N7, N8, style N10 |
| K24 | 🟢 Nit | 569–571, 682–683 | The sitemap check doesn't say whether tombstones are included, or how `/x/index.html` and `/x/` are matched. "Last updated" uses the last commit, so a code-only commit moves the date. | State both; use the last commit that touches content paths. | design N4, N8 |
| K25 | 🟢 Nit | 442–448 | The Crossref CC BY check ignores the license `start` date, so an embargoed license would pass. This is Phase 2. | Require `start` ≤ today. | design N9 |
| K26 | 🟢 Nit | whole range | There are no Markdown links; decisions and files are cited as bare text. | Link the decision files. | structural N10 |

## Contested or settled by the orchestrator

- **design N5 (CI actions unpinned, no concurrency group): contested.** The Detailed Implementation Plan (file 29) already pins each action to a release tag and sets one `pages` concurrency group. Pinning to a SHA instead of a tag is a choice, not a gap.
- **structural N3 (uneven Alternatives format):** folded into K13.
- **K8** reopens Stage 5 A9 because the leak-removal case is new.

## Orchestrator notes

- **K3 and K4 come from the C2 change** and should be fixed together. Typing a word to confirm a withdrawal, refusing a mass withdrawal, and testing the terminal check in Step 0 are small edits.
- **K2 contains a question only the vault side can answer:** does the CV builder use the same item set as the site export?
- **K5's commit-email point** depends on which `user.email` the owner commits with. The orchestrator didn't check it.
- **K11 and K12 are restructuring:** they move text without changing the design.
