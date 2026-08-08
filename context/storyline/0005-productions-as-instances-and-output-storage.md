# 0005 — Productions as instances; provider seams; SharePoint output store

> Date: 2026-08-07 · Focus: decide how *productions* (an actual music video, short,
> ad) relate to the framework, and settle where generated **output** lives. This is
> a **design/decision** entry — nothing is built yet; it records the architecture we
> agreed on before implementing it.

## The problem

`sequitur_studios` is the **engine** — a generative video-production framework we
host and evolve *in this repo*. The open question was: when it's time to actually
*make something*, how is that production represented? The rejected default was to
fork/template this repo per production — which spins up N near-identical repos
around static scaffolding that vary only in seed prompts, and freezes a copy of the
engine into each. That's the anti-pattern to avoid.

## Decisions

1. **Engine vs. instance — one repo, many lightweight productions.** The axis of
   separation is **code vs. content**. The engine (this repo: `sequitur/` +
   `artifacts/`) stays singular and evolving. A *production* is **not a repo**; it's
   a bundle of **content** (seeds, guidance, history, output) that lives in an
   **external store**. `sequitur_studios` runs as a **driver client** that connects
   to a chosen production, pulls its content, drives the pipeline, and writes
   results back. No scaffold duplication; every production rides the current engine.

2. **A production is modeled as a plan whose buckets = department layers.** Mirrors
   the same layer axis as [`context/architecture.md`](../architecture.md). Under
   each layer-bucket sit that layer's four **faces**:
   | Face | Shape | Where it lives |
   | --- | --- | --- |
   | **Seeds** | short structured text | in the plan (field/note) — deterministic fetch |
   | **History** | append-only decisions/state | in the plan (timeline/comments) — the per-production devlog |
   | **Guidance / bible** | prose corpus, RAG-queried | a doc/wiki store, *referenced* from the plan |
   | **Output** | media binaries | blob-style store, *referenced* by pointer (see #4) |

3. **The plan is the index + control plane, not a filesystem.** PM tools model
   *work* well and *payloads* poorly. Seeds + history live *in* the plan; guidance
   and output live in adjacent stores and are **linked by reference**. Never store
   bytes (especially media) in the PM tool. Platform choice (ADO's custom process
   vs. GitHub Projects v2 vs. Planner) is **deferred** — it's just one
   implementation of the read-interface below, chosen once a real production exists
   to judge it against. GitHub Projects v2 is the likely low-friction start
   (same ecosystem); ADO is the richer "custom config" option.

4. **Output storage: SharePoint (M365 tenant *Sequitur Solutions*), via Graph.**
   - **Medium:** the tenant's Business Premium **SharePoint/OneDrive** capacity —
     owned, ~TB-scale, already paid for, right-sized for this (non-large-production)
     use case, and human-browsable. **Azure Blob is deferred** — not expensive, but
     new spend/resource we don't need until output volume or delivery/CDN needs
     justify it. The Azure subscription stays in reserve for that day.
   - **Access — split by plane:**
     - *Data plane (the bytes):* **Microsoft Graph** upload (Option B) is the real
       implementation — writes from anywhere, headless/agent-safe, mints the
       pointer.
     - *Control plane (folders / share links / registry):* Graph now; an
       **MCP-over-Graph** server later (Option C) as agent-shaped convenience —
       **never the byte path** (MCP's JSON-RPC is wrong for media).
     - *Bridge for today:* a **OneDrive-synced folder** (Option A) over the
       existing [`output/`](../../output) directory validates the loop with zero API
       code, but its ceiling is a single workstation — not the destination.

5. **Two provider seams — define the interface, implement the simplest first.**
   The plan's shape and the engine's read-interface are the same object seen from
   two sides. Introduce:
   - `ProductionProvider` — `layer(name) -> { seeds, guidance_refs, history, output_refs }`.
     Impl #1 = a **local folder** (folder-per-layer = bucket-per-layer), testable
     with **zero platform commitment**. ADO/Projects providers are later swaps.
   - `OutputStore` — `put(production, layer, artifact) -> ref` where `ref` is a
     SharePoint share URL. Impl #1 `LocalFolderOutputStore` (disk; ref = path) over
     [`output/`](../../output); #2 `OneDriveSyncOutputStore` (the Option-A bridge);
     #3 `GraphOutputStore` (the Option-B real deal, swapped in behind the same seam).
   This is the same discipline as `0002`'s "make it first-class only once a second
   case justifies it," applied to the **data plane**: define the seam, ship the
   trivial provider, add MCP/Graph as alternate implementations later.

6. **Security guardrail for Graph.** No personal credentials in the engine. Register
   an **Entra app** in the Sequitur Solutions tenant with **least privilege** —
   delegated `Files.ReadWrite` for human-driven runs, or an **application permission
   scoped to the single output SharePoint site/library** for headless/agent runs —
   so secrets stay out of the engine and any model context, and an agent can't reach
   beyond the designated library.

## Resulting architecture (agreed, not yet built)

- **Plan = index** (buckets = layers; holds seeds + history + references).
- **SharePoint = output bytes** (pointer registered back into the plan).
- **Engine = driver client** reading/writing through `ProductionProvider` +
  `OutputStore` seams.
- **MCP = eventual connective tissue on the control plane** (sequitur as MCP client;
  productions/output fronted by MCP servers), added when there's ≥2 of anything to
  route between.

## Open threads

- **Build the seams:** `ProductionProvider` + `OutputStore` interfaces with the
  **local-folder** implementations first (no platform, no auth) to prove the
  driver-client loop against [`output/`](../../output).
- **Graph `OutputStore`:** stand up the Entra app (least-privilege, scoped to one
  library) and implement `GraphOutputStore`.
- **Production store platform:** decide GitHub Projects v2 vs. ADO once a first real
  production exists; until then the local provider stands in.
- Carried from `0004`: acquire *Grammar of the Edit* (editorial/sequence layer),
  broader discipline sources, first-class roles-in-code, and a `build_prompt` smoke
  test.
