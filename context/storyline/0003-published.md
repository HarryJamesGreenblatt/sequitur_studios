# 0003 — Published (public repo) + copyright hygiene

> Date: 2026-08-07 · Focus: ship the studio publicly, cleanly separating
> transformative work from verbatim copyrighted text.

## What happened

1. **Copyright hygiene (the publish blocker).** Added `.gitignore` rules for the
   verbatim book text so it never enters history:
   `artifacts/**/extraction/` and `artifacts/**/source/`.
2. **Abridged the three appendices.** `reference/appendix-a/c/d.md` had been moved
   in *verbatim*; they were the last copyrighted text in the shippable `reference/`.
   Moved the originals **back into `source/`** (now gitignored) and wrote
   **transformative** replacements under the same filenames (so `INDEX.md` /
   `architecture.md` links stay valid):
   - App. A — a short aspect-ratio history + `aspect_ratio` guidance.
   - App. C — the resource list **regrouped by department**, doubling as the
     grounding-library import backlog.
   - App. D — the crew roles as a role → department → phase table (the taxonomy
     `architecture.md` builds on).
   Result: `reference/` is now entirely transformative (6 chapters + 3 abridged
   appendices); `source/` + `extraction/` hold the verbatim ground truth, unshipped.
3. **Initialized and published.** `git init -b main`; verified staging (27 files;
   `.env` excluded, `.env.example` kept, **zero** files from `source/`/`extraction/`);
   committed; `gh repo create HarryJamesGreenblatt/sequitur_studios --public
   --source=. --push`.

## Result

**Live:** https://github.com/HarryJamesGreenblatt/sequitur_studios (public, `main`).
Secrets and verbatim copyrighted text are excluded by design; only code, docs, and
the transformative reference library ship.

## Decisions / conventions (durable)

- **Shippable vs. local:** `reference/` (transformative) ships; `source/` +
  `extraction/` (verbatim) are gitignored, local-only ground truth. Any new source
  must follow this split before it can be published.
- **No LICENSE yet** — all rights reserved by default (public-view only). Add one
  before inviting reuse/contributions.

## Open threads

- **License** — none yet; pick one (e.g. MIT) when opening to reuse.
- **Acquire *Grammar of the Edit*** → editorial/sequence layer (see App. C backlog).
- **Sequence layer**, broader discipline sources, and first-class roles-in-code
  remain future work (see `context/architecture.md`).
