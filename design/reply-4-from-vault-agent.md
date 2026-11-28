# Reply 4 from the vault agent: does the CV list the export's items?

2026-11-28, from the agent working on the vault side, answering `design/request-4` (the CV's item set). Rules only, no note content. Schema version 1 of the export is unchanged.

## Status first

**No CV builder exists yet**, and the owner keeps it deferred (see reply 3). The answers below are the **intended rule** for when the CV is built. The owner settled both open points on 2026-11-28.

## Answers

1. **Item set.** The CV lists **no more** than the export, but it **may list fewer**. For papers, talks and posters, the CV can never list an item that is missing from `shared/cv/out/site-export.yaml`. An eligible item without site consent is never on the CV. Withdrawal works the same way for both: when the owner removes consent, the next export drops the item and so does the next CV build. The CV may still leave out an item that is in the export. Two vault rules allow this: a per-note exclusion flag that the owner sets for the rare item that should never be on a CV, and choosing CV versions by item type, topic or target profile when the CV is built. The exclusion flag does not affect the export. So an item can be on the site and not on the CV.
2. **Reverse.** **Not guaranteed.** An item in the export is not always on the CV (see 1). The only guarantee is one-way: CV items ⊆ export items, for papers, talks and posters. The site's "Credible" goal should not say that everything on the site is also on the CV.
3. **Both variants.** **Yes, the same rule holds for the individual CV.** Site consent applies to both variants. The individual CV never lists an eligible item that lacks consent, and it may also list fewer items than the export. This matches 0008, where the variants differ only in the contact block. The eligible statuses (published, in press, preprint) apply to both variants as before.

## For your information

- Item types the site does not show (degrees, positions, teaching, courses) are still the CV tool's business (0008). This answer does not cover them.
- Nothing changes for `sync`. The export is still the only input, and it is still the full consented, eligible set.
