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

## Pending setup (remind me; remove each line once done)

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
