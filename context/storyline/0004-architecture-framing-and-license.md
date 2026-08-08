# 0004 — Post-publish: architecture framing + MIT license

> Date: 2026-08-07 · Focus: make the public repo's framing match the actual
> vision, and license it.

## What happened

1. **README reframed to the layered vision.** The README (and the GitHub
   description) had conveyed *Grammar of the Shot* as the whole project scope. It
   now presents the studio as a **production studio in layers** — crew
   roles/departments (Bowen App. D) across the three phases — with Grammar of the
   Shot as the **first implemented layer** (camera department, production phase).
   - Added an **Architecture** section (phase → departments → grounding → status
     table) that mirrors [`context/architecture.md`](../architecture.md).
   - Expanded **Layout** to show the grounding library (`artifacts/` + `INDEX.md`)
     and `context/` (architecture map + this devlog).
   - Reoriented the **Roadmap** by layer (editorial/post via *Grammar of the Edit*
     → sequence planner → more departments).
   - Updated the GitHub **repo description** + topics (`generative-video`,
     `filmmaking`, `cinematography`, `gemini`, `prompt-engineering`).
2. **Licensed MIT.** Added [`LICENSE`](../../LICENSE) (© 2026 Harry Greenblatt),
   a README **License** section (noting `reference/` is transformative and the
   book's verbatim text isn't distributed), and confirmed GitHub detects it as
   MIT.

## Result

Public framing now matches the architecture doc — one consistent story — and the
repo is licensed. `main` in sync with `origin/main`.

## Open threads

- Unchanged from `0003`: acquire *Grammar of the Edit* (editorial/sequence layer),
  broader discipline sources, first-class roles-in-code, and a `build_prompt`
  smoke test. See `context/architecture.md` and the OVERVIEW's Open-threads list.
