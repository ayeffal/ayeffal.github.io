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
- `/egm:egm-draft` is in progress: in `design/design_draft.md`, Overview,
  Problem, Goals and Non-Goals were approved on 2026-11-25 and no open
  questions remain. The settled items (CV PDF path from reply 3, Quarto
  `aliases:`, CC BY abstracts checked via Crossref, headshot, co-author
  requests, large files) are listed under "Settled during drafting".
- Next: draft the Technical Plan. Approving the whole design triggers the
  plugin setup below.

## Pending setup (remind me; remove each line once done)

- NEXT SESSION: resume `/egm:egm-draft` in `design/design_draft.md` with the
  Technical Plan.

- BEFORE the first commit of generated data: create the hookify rule that blocks
  commits containing DNI/CUIL patterns, absolute paths, usernames or
  non-allowlisted fields.
- WHEN the design doc is approved and building starts: install frontend-design,
  modern-web-guidance and playwright (@claude-plugins-official, project scope).
- AFTER the site scaffold exists: run claude-code-setup once.
- LATER, after adding a few items by hand: use skill-creator for an
  "add item → regenerate → review → push" skill.

At the start of each session, if a trigger above has been met, tell me before
doing anything else.
