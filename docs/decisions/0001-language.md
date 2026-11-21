# 0001. Language: English only, `/es/` reserved

Status: accepted, 2026-11-21

## Context

The site owner writes all academic documents in English. The expected
readers are international academics, collaborators and students. No
Spanish-language requirement exists in the next year. Every extra language
adds work to each new item, which conflicts with the goal of adding an item
in under 10 minutes.

## Decision

- The site is English-only at launch.
- English pages live at the root. There is no `/en/` prefix.
- The path `/es/` is reserved for a possible later Spanish version. Nothing
  else may use it.
- Language-neutral data (titles, authors, venues, dates, DOIs, URLs) is
  stored once. If Spanish is added, only free-text fields (bio, research
  summary, item descriptions, navigation labels) get an optional `es`
  version, and items without one fall back to English.
- Machine translation is never applied at build time. Any Spanish text is
  drafted by a tool if wanted, then reviewed by the owner before it is saved.

## Alternatives

- Bilingual from day one: rejected, because it doubles the writing and
  review work for no current need, and half-filled `/es/` pages look
  unfinished.
- English under `/en/`: rejected, because it makes every English link longer
  and moving English to the root later would break links.
- Automatic build-time translation: rejected, because it sends text to an
  outside service (against zero cost and privacy) and unreviewed output can
  misstate academic work.

## Consequences

- Adding Spanish later is cheap and breaks no existing link.
- Readers who do not read English are not served until that work is done.
- The data schema (decision 3) must keep translatable text fields separate
  from language-neutral fields.
