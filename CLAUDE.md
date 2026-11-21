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

## Privacy

- The vault is READ-ONLY (also enforced by a deny rule in `.claude/settings.local.json`).
- No absolute paths, usernames or machine-specific details in tracked files; those belong in CLAUDE.local.md or .claude/settings.local.json.
- Never copy anything from the vault into this repo except fields on an explicit public allowlist (to be defined in the design).
- Never commit DNI/CUIL, addresses, phone numbers, scores, amounts or raw notes.

## Decisions

Record each decision that is hard to reverse in `docs/decisions/` as a short numbered file (e.g. `0001-name.md`) with: context, decision, alternatives, consequences.

## EGM

EGM artifact directory: design/
