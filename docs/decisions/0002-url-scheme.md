# 0002. URL scheme and permanent links

Status: accepted, 2026-11-21

## Context

The site is a GitHub Pages user site. GitHub Pages cannot do server-side
redirects, so a published URL that later moves or disappears breaks every
link that others saved or cited. Academics paste links to single items in
CVs, application forms, emails, slides and papers.

## Decision

- Base URL: `https://ayeffal.github.io/`. A later custom domain is covered by
  GitHub's automatic redirect for user sites.
- Item types with their own page: **papers**, **talks** (may have
  recordings) and **posters** (the owner may upload them).
  - List: `/papers/`, `/talks/`, `/posters/`
  - Item: `/papers/<id>/`, `/talks/<id>/`, `/posters/<id>/`
- An item gets a page only when it has content to put on it: a summary
  written by the owner, or a hosted file, recording or slides. Without
  these, it is a row on its list page linking straight to the publisher
  (DOI) or its public `url`. Every public item still gets an ID, so its page
  can appear later at the reserved URL. Rows with a page show a small icon.
  Added 2026-11-21.
- Other item types (courses, software, datasets, awards) get no item
  pages. They appear as rows on list pages created when there is content. A
  page can be added later at `/<type>/<id>/` without changing existing links.
- URLs are lowercase, end in a trailing slash, and contain no dates or
  titles.
- A published URL is never removed, renamed or reused. A withdrawn paper keeps
  its page with a withdrawal notice.
- `/es/` stays reserved (see 0001).
- The format of `<id>` is set in 0003.
- **Eligible statuses** for papers: published, in press, preprint. Work in
  preparation or submitted is not eligible, and nor is a draft. A submitted
  paper with a preprint is shown as its preprint. Eligible does not mean
  public: an item appears only when the vault's export contains it (the owner
  set consent in the vault) and the manifest has an entry for it (0003, 0009).
- **Unpublished manuscripts** (submitted, in review, in preparation, draft)
  never appear on the site, as a page or as a list row, unless they have a
  preprint, and then only as that preprint. There is no override: the export
  never carries them (0008). Changed 2026-11-21: the owner-instruction
  exception was retired.

## Alternatives

- List pages only, with anchors: rejected, because anchors are not a reliable
  permanent address and cannot be cited per item.
- Item pages for every type: rejected, because pages for items with almost no
  content (awards, courses) look emptier than a list row. Posters were first
  excluded, then added on 2026-11-21 because the owner may upload them.
- Titles or dates in URLs: rejected, because titles change and preprint and
  published dates differ.
- Showing unpublished work with a "preprint soon" label: rejected, because it
  announces work before the owner or co-authors choose to.

## Consequences

- Every paper, talk and poster ID, once public, is permanent, whether or not
  its page exists yet.
- No empty item pages. A reader cannot tell from a row alone whether it has a
  page, so the icon shows it.
- Papers, talks and posters need enough fields to fill a page (0004).
- Talks and posters share one vault note type (`communication`), split by its
  `format` field, so the generator must route by `format`.
- Uploaded files (poster PDFs, recordings) need co-author consent and a
  license; decided in 0007.
- A paper becomes public only by an explicit owner action, so a new note
  never leaks by default.
