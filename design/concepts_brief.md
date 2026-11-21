# Concepts Brief: academic site (BRAINSTORM)

Material: CLAUDE.md and decisions 0001-0007. No code exists yet, so these are design-level findings.

## Reviewer status

| Reviewer | Status |
| --- | --- |
| egm-design | completed |
| egm-codebase-details | completed |
| egm-zoom-out | completed |
| egm-comprehension | completed |
| egm-implementation-readiness | completed |
| egm-structural | completed |
| egm-inventive-catalyst | completed |

## Cross-lens findings (raised by 4 or more lenses), strongest first

1. **Privacy enforcement is a local Claude hook, not a gate.** The hookify rule is pending, runs only in Claude Code, and is skipped by plain git, other machines, `--no-verify` and CI. History is irreversible (0004). Fix: a machine-readable allowlist (JSON Schema with `additionalProperties: false`) in the repo, plus a script that also checks for absolute paths, usernames and DNI/CUIL patterns. Run it as a pre-commit hook and as a CI step before deploy. Hookify becomes optional. Hard-block the first commit of generated data until it exists.

2. **The copy step is not gated by the manifest.** Nothing says the script copies only owner-approved items. If it copies every registry note and filters later, unpublished titles enter history, which is the option 0004 rejected. Fix: manifest-driven, allowlist-first extraction. Build each record from allowlisted keys and never delete fields from a copy. Items absent from the manifest are never read. CI fails on any committed record without a manifest ID and `public: true`.

3. **The pipeline is described inconsistently.** CLAUDE.md and 0004 say a script copies from the vault. 0006 says "the generator never reads the vault". There are two programs: an extractor (reads the vault, run locally) and a page build (committed files only, run in CI). Name them (for example `sync` and `build`). Scope "fail on missing field" (0003) to `sync`. Have `sync` print a report with no values or titles (copied, skipped, dropped field names, mapping failures), with a dry-run that shows the diff. Write output atomically, validate types and formats, and carry a `schema_version`. The committed data then serves as a last-good snapshot, so a vault restructure cannot break the live site. Add a "last extracted" date, and a `check` mode that reports drift between vault and committed data.

4. **The untracked ID-to-vault link file is a single point of loss.** It contradicts "rebuildable anywhere" and no lock-in, and CI can never see it. It has no backup and no consistency check. Fix: name a backup outside the repo, fail when a manifest ID has no link or a link has no ID, and verify DOI or title match after a restore. Dissent (zoom-out): public items' titles are already public, so the link can live in the tracked manifest. Only unpublished items need hiding, and those never get IDs. This removes the file entirely. It needs a ruling.

5. **Permanence has no enforcement and no takedown path.** Nothing catches a renamed ID, a dropped manifest entry, or a page demoted to a row. 0002 covers withdrawn papers but not a mistaken publish or a co-author or rights withdrawal. 0004 admits git keeps deleted files. Fix: a committed ledger of released URLs, with CI failing if any is missing from the next build. Make the manifest append-only. Define a tombstone state (page stays, content removed, notice shown) and when a history rewrite is justified. IDs are never reused. Record the risk that renaming the GitHub account breaks every URL.

6. **"Registry feeds both site and CV" is unresolved.** The site reads a filtered public subset. A real CV lists in-review and in-preparation work and uses fields the allowlist bans. Either the CV reads the vault with its own mapping or allowlist profile (two consumers), or the CV is thin. Decide now. The shared mapping file is the natural single place where a vault field becomes a named field.

7. **The 10-minute goal is untested and probably missed at first.** One item needs an ID, a manifest entry, a link entry, an authored summary, the `public` flag, sync, review, rights checks, push and CI. Nobody has totalled this. Fix: write the numbered walkthrough with time per step. Add a plain-script `add` command that proposes `surname-year-`, checks collisions and format, and writes the manifest entry, link entry and summary stub. Keep `public: true` manual. Build the command after a few manual items (as the pending list says), and promote it to a skill afterwards. If the goal is infeasible, change the goal.

8. **Findability work is absent from the decisions.** Nothing covers `citation_*` meta tags, schema.org Person and ScholarlyArticle JSON-LD, an ORCID link, a sitemap, `robots.txt`, a canonical URL, a homepage research summary, or any contact route (deferred in 0007). Row-only items link away and add little to search. A Google Scholar-style signal needs a crawlable PDF, which conflicts with the rights rule. Decide Search Console verification (no tracker) as a free signal.

9. **Quarto weight and drift (about 476 MB).** CI, PDF output and real icons are untested. Fix: run an end-to-end CI build on fake data with a cache and pinned action versions. Keep logic in Python and templates thin. Change the pin in its own commit with an output-tree diff. Fail on Quarto warnings and on version mismatch. Dissent (zoom-out): the Python script could render static HTML directly, and the "one toolchain for the CV" argument was dropped in 0006. At minimum, defer the choice until the CV is built.

## Contested or single-lens findings

- **Hosting PDFs in git (design, zoom-out, structural).** History cannot be cleaned and the size has no cap. Options: per-file cap and total budget, a CI check for PDF metadata, and a rights-note plus consent-confirmed flag per file that fails the build when missing. Or use Zenodo or an institutional repository (free, DOIs, versioning) and skip in-repo files for v1.
- **Two visibility controls (comprehension, catalyst, codebase-details).** The `public` flag (0004) and "explicit owner instruction naming the manuscript" (0002) are not clearly one switch. Proposal: a separate required field such as `owner_approved_unpublished: <date>` that CI checks against a carried-through vault status. Define what the assistant may set, since an AI edits the files.
- **Redirects.** Catalyst notes Quarto `aliases:` writes meta-refresh stubs, weakening the "Pages cannot redirect" premise (weaker than a 301). Tradeoff: stubs accumulate. Verify before relying on it.
- **Standard bibliographic format (zoom-out).** Use CSL-JSON plus per-item YAML instead of a bespoke schema. Caveat: "Yeffal A" is not structured family and given names.
- **Assign IDs only when a page is created (zoom-out).** Rows have no URL, so there is nothing to protect. Conflicts with 0002's "every public item gets an ID". Needs a ruling.
- **Scope reduction (zoom-out).** Papers first. Talks, posters, `related` links, per-field Spanish fallback and Playwright could wait.
- **Derive "has page" in one place (structural).** The rule is spread over 0002, 0004 and 0006. Compute it in the generator and never store it. Add an accessible text label, not only an icon.
- **Lifecycle table (implementation-readiness).** Specify what happens when a preprint gains a DOI, a page loses its summary or file, the first author changes, or `related` points to a non-public item. Fail the build on the last.
- **Regeneration vs authored text (codebase-details).** Say that regeneration never touches authored files, and fail if one has no manifest entry.
- **Post-deploy and link health (codebase-details).** A smoke check on the live site, and a weekly external link check that opens an issue.
- **Co-author names are third-party personal data.** State how someone can ask for removal.
- **License interaction (design).** CC BY 4.0 is irrevocable. A summary that paraphrases a publisher abstract may carry third-party rights.
- **Guard `/es/` (structural).** A build check that nothing else writes under it.

## Inventive resolutions

- **Segmentation.** Stage 1 `sync` (local, vault, link file, mapping) writes committed data. Stage 2 `build` (CI, anywhere) needs a clone and pinned Quarto only. This resolves "rebuildable anywhere" versus the untracked link file, and makes vault drift a local failure.
- **Structural privacy.** An allowlist-built record plus `additionalProperties: false` makes a leak a validation failure rather than something to remember.
- **Page versus file.** Keep the page URL permanent and make the file removable, leaving a tombstone.
- **CV profile.** One mapping file with two allowlist profiles: public (committed) and CV (local, not committed).

## Nits

- Stale cross-references: 0001 and 0002 say "decision 3" for the schema (it is 0004). 0002 and 0004 say "decision 6" for licenses (it is 0007). Use file numbers.
- 0004 is "accepted" with an open point.
- `LICENSE` and the content notice do not exist yet and are needed before the first deploy.
- `docs/` is untracked.
- The ID year ("first public version on the site") is ambiguous (site year or paper year?) and cannot be checked. It needs worked examples and a collision rule.
- Undefined terms: registry, manifest, mapping file, local link file, authored text, hookify, `communication`, and the values of `format`. Add a glossary and a repo layout.
- Error messages for each failure case (missing field, duplicate ID, public item without summary, missing rights note, missing link file on a fresh clone) are unspecified.
- Validate that `url` is a public https link. Date format and time zone are unspecified.
- Pin the Python dependencies.
- 0001's translatable-field split does not appear in the 0004 schema.

## Not checked

No reviewer inspected the vault, Quarto behaviour, CI, or any code (none exists). Pages limits, `aliases:` behaviour and CSL author compatibility are from general knowledge. The decision files were not edited.
