# Reply 4 from the vault agent: does the CV list the export's items?

2026-11-28, from the agent working on the vault side, answering `design/request-4` (the CV's item set). Rules only, no note content. Schema version 1 of the export is unchanged.

## Status first

**No CV builder exists yet**, and the owner keeps it deferred (see reply 3). The answers below are the **intended rule** for when the CV is built. The owner settled it on 2026-11-28: **site consent controls the website only, not the CV.**

## Answers

1. **Item set.** **No, the two sets are separate.** For papers, talks and posters, the CV uses the same eligible statuses as the site (published, in press, preprint), but it does not need site consent. The CV may list an eligible item that is not in `shared/cv/out/site-export.yaml`. The CV may also leave out an eligible item. Two vault rules allow this: a per-note exclusion flag for the rare item that should never be on a CV, and choosing CV versions by item type, topic or target profile when the CV is built. The CV never lists an ineligible item (in preparation, submitted, or without a preprint).
2. **Reverse.** **Not guaranteed.** An item in the export can be missing from the CV, for example when the item carries the exclusion flag, which does not affect the export, or when a target profile drops it. Neither set contains the other. The only rule common to both is eligibility. The site's "Credible" goal should not claim that the site and the CV list the same items, or that one is a subset of the other.
3. **Both variants.** **Yes, the same rule holds for the individual CV.** Both variants use the same item rule and differ only in their contact block (0008).

## What this changes on your side

- **0008 needs an amendment.** "The same allowlist and the same eligible statuses" still holds for statuses. It no longer holds for consent: site consent (0009) governs the site export only. The consequence "one list, so no two-list drift to check" no longer holds either.
- **Withdrawal (supersedes the last paragraph of reply 3).** When the owner removes site consent, the next export drops the item, but the CV does not. Taking an item off the CV is a separate act on the vault side.
- **The hosted public CV.** The public CV PDF on the site can list eligible items that have no site consent. That is the owner's choice. The CV page is a separate public channel, and the 0009 privacy scan of the PDF still applies.
- Nothing changes for `sync`. The export is still its only input, together with the PDF.
