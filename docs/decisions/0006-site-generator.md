# 0006. Site generator: Quarto

Status: accepted, 2026-11-21

## Context

The owner knows Python and R, not Ruby or Go. The site must be rebuildable
anywhere with plain files. A PDF CV tool is still being built and reads the
same registry data. The vault is private, so a script generates item files
locally and they are committed; the generator never reads the vault.

## Decision

- The site is built with **Quarto**, pinned to a specific version (tested
  with 1.11.9) in CI and in the repo docs.
- Each item that has a page lives in `<type>/<id>/index.qmd`, which builds
  to `/<type>/<id>/` as required by 0002.
- List pages use Quarto listings from a data file. Rows without a page link
  straight to the publisher or public `url`. Rows with a page link to it.
- A Python script, not Quarto, turns allowlisted data into those files (0003,
  0004).
- Deployment uses a GitHub Actions workflow with the pinned Quarto version.
- The PDF CV is not tied to Quarto. It may use Quarto or Typst later and
  reads the same data.

## Alternatives

- Hugo: smaller, one program, and it makes the URLs by default. Rejected
  because the owner would not be able to maintain its Go templates, and the
  CV advantage of one toolchain was real.
- Jekyll: rejected because it needs Ruby, can't make PDFs, and its
  GitHub-built benefit is lost when the data is generated locally.

## Consequences

- The dependency is large (about 476 MB unpacked) and Quarto changes between
  versions, so the version must be pinned and upgraded deliberately.
- Pages carry Bootstrap and some JavaScript.
- Tested with fake items: URLs of the form `/papers/<id>/`, and one list
  mixing external and internal links. Not tested: PDF output, a CI build, a
  real icon for rows that have pages (a text column worked), and
  long-term maintenance.
- If a limit appears later, the item files and data are plain Markdown and
  YAML, so moving to Hugo means rewriting templates only.
