# ayeffal.github.io — academic website

GitHub Pages user site. The private notes vault (attached via .claude/settings.local.json) is the source of truth.

## Goals

- A findable, credible academic home.
- Registry notes in the vault are the single source of truth for both the site and the PDF CV.
- Zero cost and no lock-in: plain files, rebuildable anywhere.
- Private by construction.
- Adding an item takes under 10 minutes.

## Non-goals (for now)

Blog, analytics, trackers, comments, forms, custom domain.

## Rules

- Make the smallest change that fully solves the task.
- No unrequested features, abstractions or dependencies.
- End each reply with what you skipped or didn't verify.
- Before any commit or push, run `git remote get-url origin`. If it isn't
  `https://github.com/ayeffal/ayeffal.github.io.git`, stop and tell me.

## Privacy

- The vault is READ-ONLY (also enforced by a deny rule in `.claude/settings.local.json`).
- No absolute paths, usernames or machine-specific details in tracked files; those belong in CLAUDE.local.md or .claude/settings.local.json.
- Never copy anything from the vault into this repo except fields on an explicit public allowlist (to be defined in the design).
- Never commit DNI/CUIL, addresses, phone numbers, scores, amounts or raw notes.

## Decisions

Record each decision that is hard to reverse in `docs/decisions/` as a short numbered file (e.g. `0001-name.md`) with: context, decision, alternatives, consequences.

## EGM

EGM artifact directory: design/

## Where things stand (update when it changes)

- Design phase, no site code yet. Decisions 0001-0010 are in `docs/decisions/`; the summary and open items are in `design/concepts_brief.md`.
- The vault agent has answered: consent lives in the vault, records are keyed by `uid`, export schema version 1 (`design/reply-from-vault-agent.md`, `design/reply-2-from-vault-agent.md`). The input schema and tests are in `sync/`. Decisions 0002, 0003, 0004, 0008 and 0009 are updated.
- Design approved on 2026-11-25: `design/academic-website.md` (final;
  `design/design_draft.md` is the working copy it was saved from). Summaries
  are written site-side, `sync` generates committed pages, one writer per
  file. Updates to 0004, 0006 and 0009 are step 10 of its Order of work.
- EGM review in progress (interactive, all rubrics). Stage 5 done
  (`design/zoom_out_report.md`); its findings were applied to the design on
  2026-11-26 (pre-push hook, ledger holds page URLs only, no `aliases:`,
  Phase 2 for CC BY abstracts and hosted files). Stage 6 done
  (`design/comprehension_report.md`), all findings applied; C2 changed the
  design on 2026-11-27: `sync` suggests each ID and writes the manifest
  after the owner confirms. Stage 7 done (`design/critic_report.md`); its
  fixes were decided interactively and applied on 2026-11-28 (decisions at
  the top of `design/goldfish_review_report.md`). K4 changed the design:
  `sync` never prompts; new IDs and withdrawals are confirmed by the owner
  in a gitignored `sync-pending.yml`. K2b answered 2026-11-28
  (`design/reply-4-from-vault-agent.md`, revised): site consent governs the
  site only; CV and site share the eligibility rule, neither item set
  contains the other. Applied to the Credible goal and 0008. Next: Stages 8
  and 9, then Step 0 (Quarto spike; Quarto is not installed yet).

## Pending setup (remind me; remove each line once done)

- BEFORE the first commit of generated data: create the hookify rules (design
  file 33): one blocks shell writes to owner files, one blocks bypassing the
  git hooks (`--no-verify`, `core.hooksPath`, edits to `.githooks/`). The
  privacy patterns live only in `checks/privacy.py`.
- WHEN the design doc is approved and building starts: install frontend-design,
  modern-web-guidance and playwright (@claude-plugins-official, project scope).
- AFTER the site scaffold exists: run claude-code-setup once.
- LATER, after adding a few items by hand: use skill-creator for an
  "add item → regenerate → review → push" skill.

At the start of each session, if a trigger above has been met, tell me before
doing anything else.
