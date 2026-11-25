# 0010. Site pages and home-page affiliation

Status: accepted, 2026-11-21

## Context

Search committees, collaborators and editors look up a candidate's name. The
site should be the canonical page that joins the owner's papers, ORCID and
affiliations. It is also limited by the goals in CLAUDE.md: no blog, no
analytics, no forms.

## Decision

Five pages:
1. **Home**: name (0005), affiliation line, a short plain-language research
   paragraph, the contact address (0008), and links to ORCID and Google
   Scholar.
2. **Research**: a short plain-language description of the owner's topics.
3. **Papers**: `/papers/` (0002).
4. **Talks and posters**: `/talks/` and `/posters/` (0002).
5. **CV**: the public PDF (0008).

The home-page affiliation lines (English, matching the owner's PLOS Biology
paper and the supervisor's English CV):

> Doctoral fellow, CONICET · PhD candidate, School of Medicine, University of Buenos Aires (UBA)
> Physiology of Action Lab, ICIFI, School of Science and Technology (ECyT), University of San Martín (UNSAM)

- The doctoral program is **not named** on the page. Colleagues' and the
  supervisor's CVs do not name theirs, and the faculty and university say
  enough. Its confirmed Spanish name, for any page that needs it, is
  *Doctorado en Ciencias Médicas Básicas*.
- ORCID iD `0000-0002-9645-6664`, linked on the home page and in the page
  metadata.
- Google Scholar: the home page links one profile,
  `https://scholar.google.com/citations?user=vT8iym4AAAAJ`, kept on the
  owner's personal Google account so it survives job changes. The other
  profile was deleted on 2026-11-21 after the owner found the two identical.
  Profile settings (set in Scholar, not in this repo): affiliation
  `Physiology of Action Lab, ICIFI, Universidad Nacional de San Martín
  (UNSAM)`; verification email at the new institutional domain; interests
  limited to published topics (motor learning, hippocampus, memory
  consolidation, diffusion MRI, neuroplasticity); homepage set to this site
  once it is live. Two-step verification should be on.
- No former affiliation (IFIBIO) on the home page.
- The Spanish official names go in hidden page metadata and in a small "in
  Spanish" line on the Research page, so search engines see both forms:
  *Instituto de Ciencias Físicas (ICIFI), Escuela de Ciencia y Tecnología
  (ECyT), Universidad Nacional de San Martín (UNSAM)* and *Facultad de
  Medicina, Universidad de Buenos Aires*. Use correct accents, even where the
  owner's papers dropped them.
- Roles with no official English name keep the Spanish term, as in the
  supervisor's CV: `Teaching Assistant (Ayudante de Segunda)`.

No teaching page (the owner is not teaching this year). No separate contact
page: the footer carries the contact line. Decided 2026-11-24: the home
page shows a headshot the owner holds the rights to (own photo, or the
photographer's written permission), with its metadata stripped before commit.

## Alternatives

- Single page: rejected, because lists of papers and talks need their own
  URLs (0002).
- Teaching, software, news and blog pages: not now. A page can be added later
  without changing existing URLs.

## Consequences

- The owner writes the home and research text. It cannot come from the vault.
- A new `github.io` site is indexed slowly. Registering it with search
  engines and linking it from ORCID and Scholar will help; neither is done.
  Decided 2026-11-24: register the site with Google Search Console (ownership
  proved by a meta tag or HTML file in the repo, then the sitemap submitted)
  and import it into Bing Webmaster Tools. This adds no tracker to the pages.
- Not verified: the form "University of San Martín" against UNSAM's own
  pages (they could not be read), and whether CONICET's 2016 affiliation
  resolution covers websites. It was confirmed only for publications. The
  UBA resolution cited in a research file could not be reached.
- An unmaintained site looks worse than none, so the home page shows the
  date of the last update.
