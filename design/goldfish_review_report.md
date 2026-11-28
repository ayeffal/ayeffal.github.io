# Goldfish Annotated Review Report

**Target:** `design/academic-website.md` (lines 1–838, the FeatureRange). Findings come from `design/critic_report.md` (Stage 7).

**Counts:**
- PROPOSE FIX: 23 (one of them, K2, also has a part to escalate)
- ESCALATE: 1 (K2b)
- CONTEST: 1 (design N5, already settled in the critic report)
- DECLINE: 2 (K21, K26)

## Owner decisions (interactive, 2026-11-28)

*   **Accepted as proposed:** K1, K2a, K5, K6, K7, K8, K9, K10, K11, K12,
    K14, K16–K20, K22–K25.
*   **K3, accepted without the threshold:** the withdrawal default is "no"
    and it needs the word `withdraw`; `sync` stops on an empty export; no
    `--allow-many-missing`.
*   **K4, replaced by a confirmation file:** the owner doesn't want to type
    into a running command. `sync` drops terminal prompts entirely. When
    there are new IDs or withdrawals to confirm, it writes a gitignored
    `sync-pending.yml` (marked PENDING), stops with a warning and writes
    nothing else.
    *   The owner sets `confirm: yes` for each new item, after editing the
        suggested `id` if wanted, or `confirm: withdraw` for each withdrawal.
        `sync` then runs again.
    *   It finishes only when every entry is confirmed, then deletes the file.
    *   If the export changed in between, answers are kept for entries that
        still apply.
    *   Claude's tools are denied on the file. The pre-commit hook refuses a
        commit while it exists.
*   **K13, accepted:** the alternatives also include "confirm at a terminal
    prompt" (rejected 2026-11-28).
*   **K15, accepted:** skip and quit are not needed with the file (leaving
    `confirm: no` skips the entry). An empty `id` is left when both tag
    words are taken. Compound surnames become hyphenated (`de-la-fuente`).
*   **Declined (agreed):** K21, K26, design N5.
*   **K2b:** sent to the vault agent (`design/request-4-to-vault-agent.md`).

## Escalated: needs the owner's knowledge

### [K2b] [`egm-design`] - Severity: Major
*   **Affected Scope:** lines 90–96 (Goals, "Credible")
*   **Discrepancy Description:** No source shows whether the vault's CV builder lists exactly the items the site export holds. The export holds only items with site consent (0008, 0009). The CV uses "the same allowlist and the same eligible statuses" (0008), but 0008 doesn't say the CV is limited to items with site consent.
*   ***AI Suggestion:*** ESCALATE
*   ***Justification:*** Only the vault side knows this. No file in this repo answers it.
*   ***Proposed Edit:*** none until answered. If the CV can include items without site consent, the goal says "every item on the site is also on the CV", not "the same items".

## Prioritized Findings & AI Suggestions

### [K1] [`design`, `structural`, `style`] - Severity: Major
*   **Affected Scope:** lines 9–11, 658–675 (Decision updates this plan needs)
*   **Discrepancy Description:** The list leaves out 0003, the C2 changes to 0009, the visibility change to 0004, and the 0007 license location. Line 11 points to step 10, which is outside the range.
*   ***AI Suggestion:*** PROPOSE FIX
*   ***Justification:*** Valid. The list must match step 10, and it must name every decision whose text this design contradicts.
*   ***Proposed Edit:***
    *   Lines 9–11: "…go into the decisions listed under 'Decision updates this plan needs' (Technical Plan)."
    *   Add **0003** (2026-11-27): `sync` suggests each ID and the owner confirms or retypes the tag; the year is the year of the record's `date` when the ID is made; the manifest is written by `sync`.
    *   Add **0007**: the license record is in `data/abstract-licenses.yml`, not in the authored file.
    *   Extend **0004**: the visibility rule is the vault consent, plus the owner's confirmation at `sync`'s ID prompt.
    *   Extend **0009** (2026-11-27): `sync` doesn't finish while an exported item has no ID, so the "reports the rest as counts" rule is replaced. The owner confirms a withdrawal at `sync`'s prompt, and `sync` adds the `withdrawn` date.

### [K2a] [`style`, `design`, `structural`] - Severity: Major
*   **Affected Scope:** lines 90–96, 175–177
*   **Discrepancy Description:** "The site cannot lag behind the CV" is true only right after a `sync`.
*   ***AI Suggestion:*** PROPOSE FIX
*   ***Proposed Edit:***
    *   Goal: "…the site and the public CV draw on the same vault records and eligibility rule (0008, 0010). After each `sync`, every item in the export is on the site. Check: `sync` stops if any exported item has no manifest entry…"
    *   Line 175–177: "…and `sync` cannot finish with an exported item left off the site."

### [K3] [`design`] - Severity: Major
*   **Affected Scope:** lines 404–410, 503–508, 637–644
*   **Discrepancy Description:** A broken or empty export offers to withdraw everything, the default answer isn't stated, and a pushed withdrawal can't be undone.
*   ***AI Suggestion:*** PROPOSE FIX
*   ***Justification:*** This risk is new from C2. The fix is small and closes it.
*   ***Proposed Edit:***
    *   The withdraw prompt defaults to "no", and withdrawing needs the word `withdraw` typed in full.
    *   If the export has no items while the manifest has entries that aren't withdrawn, `sync` stops before asking anything ("export looks empty").
    *   If more than 2 items are missing at once, it stops unless `--allow-many-missing` is given.
    *   State the consequence: once pushed, a withdrawal is permanent. The item can't return under the same `uid` or ID.
    *   Add a risk row for this.

### [K4] [`design`] - Severity: Major
*   **Affected Scope:** lines 385–388, 503
*   **Discrepancy Description:** The terminal check can be faked. Native Python under Git Bash (mintty) may not see a terminal at all.
*   ***AI Suggestion:*** PROPOSE FIX
*   ***Proposed Edit:***
    *   Reword: "`sync` asks only when stdin is an interactive terminal. This keeps an agent's run from answering by accident; it is not a security control. The real control is that every new entry shows up in the commit diff the owner reviews."
    *   Add Step 0 row #11: the prompt works when the owner runs `sync` from Git Bash and from PowerShell. Fallback: `--confirm-ids` reads the answers from a prompt file the owner edits.
    *   Add a risk row.
    *   The suggested hookify rule is left out, as an unrequested extra.

### [K5] [`style`, `design`] - Severity: Major
*   **Affected Scope:** lines 103–112, 551–554
*   **Discrepancy Description:** The goal overclaims. The binary check is narrow. The commit email is public.
*   ***AI Suggestion:*** PROPOSE FIX
*   ***Justification:*** The orchestrator checked: this clone commits with a GitHub noreply address, so the email point is a risk to record, not a current leak.
*   ***Proposed Edit:***
    *   Goal: "The local hooks refuse a commit, and CI refuses a deploy, if… The username check runs only in the local hooks. The hooks can be skipped on purpose (see 'What the hooks cannot do')."
    *   Binary check (3): add "Phase 2 hosted PDFs: the strip tool also drops annotations and embedded files; a PDF with images but no extractable text is refused until the owner confirms it."
    *   Risk rows:
        *   Commit metadata is public. The repo commits with the GitHub noreply address; keep it that way.
        *   Image data inside a PDF isn't re-encoded.

### [K6] [`design`] - Severity: Major
*   **Affected Scope:** lines 536–547 (Checks, 2)
*   **Discrepancy Description:** `.claude/settings.json`, `CLAUDE.md`, `.githooks/`, `.gitignore`, `.gitattributes` and `requirements.txt` aren't scanned, and these are the files where absolute paths usually build up.
*   ***AI Suggestion:*** PROPOSE FIX
*   ***Proposed Edit:*** "The absolute-path and username checks also run on `.claude/`, `CLAUDE.md`, `.githooks/`, `.github/`, `.gitignore`, `.gitattributes` and `requirements.txt`. These files hold no vault data but are where machine paths creep in."

### [K7] [`design`] - Severity: Major
*   **Affected Scope:** lines 542–550
*   **Discrepancy Description:** The postal-code and phone patterns would match years, page ranges and volumes.
*   ***AI Suggestion:*** PROPOSE FIX
*   ***Proposed Edit:***
    *   "Phone numbers: a `+54` prefix, or 8 or more digits in groups split by spaces or dashes, outside a `pages` field. Postal codes: only the CPA form (a letter, four digits, three letters); the old four-digit form is not scanned, because it can't be told apart from a year."
    *   "Every pattern is tested against the sample export and the generated pages, which must pass clean."
    *   Add a risk row: four-digit postal codes aren't caught.

### [K8] [`design`] - Severity: Major
*   **Affected Scope:** lines 558–560, 579–590
*   **Discrepancy Description:** A history rewrite for a leak (allowed by 0009) fails the append-only check in CI. CI's baseline isn't defined for every case.
*   ***AI Suggestion:*** PROPOSE FIX
*   ***Proposed Edit:*** Append to check 5:
    *   "CI's baseline is the commit before the push. If there is none (the first push or a manual run), or it isn't an ancestor of the pushed commit (a force push after an approved rewrite), CI skips this check and says so in the log."
    *   "A leak is removed with `git filter-repo`, approved by the owner each time (0009). The rewritten commits never contained the entry, so the pre-push hook, which compares each commit with its parent, passes them."

### [K9] [`style`, `design`] - Severity: Major
*   **Affected Scope:** lines 113–121, 345, 454–455, 632–633
*   **Discrepancy Description:** The goal is wider than its check, and four different words are used for when a URL becomes permanent.
*   ***AI Suggestion:*** PROPOSE FIX
*   ***Justification:*** The ledger already includes the fixed pages (`FIXED_PAGES`, Detailed Plan file 14), but the feature range never says so.
*   ***Proposed Edit:***
    *   Goal: "Every page URL that has been pushed (an item page, a list page, the home, research or CV page) keeps reaching its page or a tombstone."
    *   Ledger definition (345, 454): "every page URL ever generated, including the fixed pages". Use "pushed" for the moment a URL becomes permanent, with 632–633 as the single definition.

### [K10] [`style`] - Severity: Major
*   **Affected Scope:** lines 209–213
*   **Discrepancy Description:** "A missing summary is never an error" contradicts the Lifecycle row for a page that loses its content. Line 210 also still puts the license record "in the authored file".
*   ***AI Suggestion:*** PROPOSE FIX
*   ***Proposed Edit:*** "…the license URL, DOI and check date are recorded in `data/abstract-licenses.yml`… A summary is optional: one never written is never an error. Removing the only content of a pushed page is an error (see Lifecycle)."

### [K11] [`structural`] - Severity: Major
*   **Affected Scope:** lines 677–697
*   **Discrepancy Description:** There is no Risks & Mitigations section, several risks have no mitigation, and scale isn't covered.
*   ***AI Suggestion:*** PROPOSE FIX
*   ***Proposed Edit:***
    *   Make "Risks and unverified points" an H2, "Risks and Mitigations", just before Alternatives.
    *   Write each risk as "risk → mitigation". Examples:
        *   Quarto untested → Step 0, falling back to Alternative D.
        *   Scholar → only the citation tags are under our control; checked after launch with Scholar's own lookup.
        *   Scan meaning → the owner reads every diff before committing.
    *   Add rows:
        *   hooks skipped (points to "What the hooks cannot do");
        *   mistaken withdrawal (K3);
        *   terminal check (K4);
        *   commit email and PDF images (K5);
        *   four-digit postal codes (K7);
        *   scale: PDFs build up in git history → 5 MB cap and Phase 2 only. GitHub Pages' published-site limit is 1 GB.

### [K12] [`structural`] - Severity: Major
*   **Affected Scope:** lines 149–246
*   **Discrepancy Description:** Open Questions holds settled design. The ID-suggestion rule appears only there.
*   ***AI Suggestion:*** PROPOSE FIX
*   ***Proposed Edit:***
    *   Keep "## Open Questions / None remaining."
    *   Turn the two subsections into a new H2, "## Settled Choices". Line 155 becomes "Each is part of the Technical Plan; dates show when it was settled."
    *   Move the ID-suggestion rule into Data formats, under `data/manifest.yml`, leaving a one-line pointer behind.

### [K13] [`structural`, `design`] - Severity: Major
*   **Affected Scope:** lines 718–806
*   **Discrepancy Description:** "Rejected by author" has no linked record, and the C2 choice has no alternative entry.
*   ***AI Suggestion:*** PROPOSE FIX
*   ***Proposed Edit:***
    *   A–F: "Rejected (owner, 2026-11-25): …" or "Rejected ([0006](../docs/decisions/0006-site-generator.md)): …", with each decision file linked.
    *   Add Alternative I, "Owner types each manifest entry by hand":
        *   Pros: the owner picks every tag, with no prompt code.
        *   Cons: copying the `uid` from the export file is slow and error-prone, and the site lags the export until it's done (Stage 6 C2).
        *   Rejected: owner, 2026-11-27.

### [K14] [`style`] - Severity: Major
*   **Affected Scope:** lines 176–179
*   ***AI Suggestion:*** PROPOSE FIX
*   ***Proposed Edit:*** Drop "as in common academic-site practice, where being in the curated data file means being shown."

### [K15] [`design`] - Severity: Nit
*   **Affected Scope:** lines 167–176
*   ***AI Suggestion:*** PROPOSE FIX
*   ***Proposed Edit:*** Add these rules:
    *   Title words are reduced to ASCII letters, and a word left empty is skipped (`2D` becomes `d`, so it is skipped as too short; words under 3 letters are skipped).
    *   If both words of the tag are taken, `sync` gives no suggestion and the owner types one.
    *   Typed tags are checked against the regex.
    *   Answer `s` to skip the item for this run, which makes the run stop at the end without writing; answer `q` to quit at once.
    *   The year is the year of the record's `date` when the ID is made (the reading of 0003).

### [K16] [`all`] - Severity: Nit
*   **Affected Scope:** lines 3–12, 153, 250
*   ***AI Suggestion:*** PROPOSE FIX
*   ***Proposed Edit:***
    *   Status: "Approved 2026-11-25; review amendments 2026-11-26 and 2026-11-27, approved by the owner during the EGM review."
    *   Move the "Dates in parentheses" note below Date.
    *   Heading: "Settled during drafting (2026-11-24, later amendments dated inline)".
    *   Rename "Settled before drafting (2026-11-25)" to "Settled before drafting the Technical Plan (2026-11-25)".

### [K17] [`structural`, `style`] - Severity: Nit
*   **Affected Scope:** lines 43–55
*   ***AI Suggestion:*** PROPOSE FIX
*   ***Proposed Edit:*** Add **manifest**, **ledger**, **tombstone**, **Phase 2**, **Step 0** (the Quarto test before building, in the Detailed Implementation Plan) and **`build`** (the CI job) to "Terms used below".

### [K18] [`structural`] - Severity: Nit
*   **Affected Scope:** lines 290–292
*   ***AI Suggestion:*** PROPOSE FIX
*   ***Proposed Edit:*** Diagram line: "new uids: owner confirms an ID; missing uids: owner confirms withdrawal".

### [K19] [`style`] - Severity: Nit
*   **Affected Scope:** lines 115, 319, 489, 581, 655, 803
*   ***AI Suggestion:*** PROPOSE FIX
*   ***Proposed Edit:***
    *   Drop "with foresight".
    *   "like with like" becomes "the same version of each file".
    *   "nobody asked for" becomes "not wanted".
    *   "the real privacy gate" becomes "the privacy gate".
    *   "the riskiest part" becomes "the part most likely to leak co-author data".

### [K20] [`style`] - Severity: Nit
*   **Affected Scope:** lines 123, 320, 618
*   ***AI Suggestion:*** PROPOSE FIX
*   ***Proposed Edit:***
    *   "Quarto 1.11.9 (pinned, not yet tested)".
    *   "a file staged only in part is checked as staged".
    *   Heading: "Adding an item (target: under 10 minutes)".
    *   Line 386 is handled by K4.

### [K21] [`style`] - Severity: Nit
*   ***AI Suggestion:*** DECLINE. K17 defines `build` as the CI job, which covers it.

### [K22] [`structural`, `style`] - Severity: Nit
*   **Affected Scope:** lines 113–121
*   ***AI Suggestion:*** PROPOSE FIX
*   ***Proposed Edit:*** Move "Pages do not move… Hosted files are not in the ledger…" before "Check:" (done together with K9).

### [K23] [`structural`, `style`] - Severity: Nit
*   **Affected Scope:** lines 72, 115, 123, 359, 524, 610; 66; 516–525
*   ***AI Suggestion:*** PROPOSE FIX
*   ***Proposed Edit:*** Rewrap those lines, use `1.  ` at line 66, and put the hooksPath sentence in its own paragraph.

### [K24] [`design`] - Severity: Nit
*   **Affected Scope:** lines 566–571
*   ***AI Suggestion:*** PROPOSE FIX
*   ***Proposed Edit:***
    *   "`sitemap.xml` lists every built page except tombstones; `/x/index.html` and `/x/` count as the same URL."
    *   Use the date of the last commit that touched `data/`, `authored/` or a shell (`git log -1 --format=%cs -- data authored '*.qmd'`).

### [K25] [`design`] - Severity: Nit
*   **Affected Scope:** lines 442–448
*   ***AI Suggestion:*** PROPOSE FIX
*   ***Proposed Edit:*** "…a CC BY license whose `start` date is on or before today."

### [K26] [`structural`] - Severity: Nit
*   ***AI Suggestion:*** DECLINE. Bare decision numbers are used across all ten decision files and the brief. K13 links them where a rejection is attributed.

### [design N5] - Severity: Nit
*   ***AI Suggestion:*** CONTEST (already in `critic_report.md`). Detailed Plan file 29 pins each action to a release tag and sets a `pages` concurrency group.
