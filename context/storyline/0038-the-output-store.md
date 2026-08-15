# 0038 — The Output Store

> Date: 2026-08-15 · Focus: **code** — built the long-deferred **`OutputStore`** seam
> (`0005`), the **data plane** the `0036` dailies model needs so each phase's deliverable
> persists **by reference**, is shown at a gate, and is comparable across revisions. A
> `runtime_checkable` `OutputStore` Protocol + one `LocalFolderOutputStore` backend rooted
> at the OneDrive-synced `OUTPUT_STORE_ROOT` — so "local disk" already buys tenant
> durability, with no API code and no new dependency. 45 tests green.

---

## What happened

The `0036` reframe put the **`OutputStore`** at the top of the critical path: every later
phase (treatment, poster, storyboard, dailies, cut) persists its deliverable *by reference*,
and revise-don't-restart needs those references to survive across iterations. `0005` reserved
the seam (`put(production, layer, artifact) -> ref`) but nothing had been built. This session
built it — the studio's **third seam**, one per plane:

| Plane | Seam | Shape |
|---|---|---|
| execution | `sequitur.render.Renderer` | a decision → **new bytes** |
| control | `sequitur.production.ProductionProvider` | board tree ↔ `Brief` / `Sequence` |
| **data** | **`sequitur.output.OutputStore`** | **produced bytes → a durable `ref`** |

- **`sequitur/output.py`** — a `runtime_checkable` `OutputStore` Protocol
  (`put(artifact, *, production, layer, name=None) -> Path | str`) and one backend,
  `LocalFolderOutputStore`, which files each artifact at `<root>/<production>/<layer>/<name>`
  and returns that path. `artifact` is **either raw `bytes` or a path** to a freshly rendered
  file (exactly what a `RenderResult.ref` carries), so the store sits directly downstream of
  the execute-hook (`0032`): render to scratch → `put` into the durable store.

- **`config.get_output_store_root()`** — resolves `OUTPUT_STORE_ROOT` (in `.env`) or fails
  loudly, mirroring `get_ado_config`. The backend takes an explicit `root` (like
  `LocalFolderProduction(path)`) and falls back to that resolver — so tests point at a temp
  dir and production points at OneDrive, from the same class.

- **Public surface + test.** Exposed `OutputStore` / `LocalFolderOutputStore` on the package.
  `tests/test_output.py` (6) covers the round trip offline against a temp root: protocol
  conformance, `put` bytes, `put` a rendered path (copies in, leaves the scratch intact, name
  defaults to the source filename), explicit-name override, the bytes-without-a-name error, and
  the env-pointer default root. Suite **45 green** (was 39).

- **Live-verified** through the *real* root: `LocalFolderOutputStore().put(b"…",
  production="_probe", layer="plan", name="marker.txt")` landed at
  `…\OneDrive - Sequitur Solutions\Sequitur Studios\output\_probe\plan\marker.txt`, read back
  identical, probe removed. The OneDrive junction (`0036`) means this single disk backend is
  already the durability bridge.

## Decisions

1. **One backend does double duty (disk + durability).** `0005` sketched three impls
   (LocalFolder → OneDriveSync → Graph). With `OUTPUT_STORE_ROOT` pointed at a OneDrive-synced
   folder, `LocalFolderOutputStore` **is** the Option-A bridge — free tenant durability with no
   API code. `GraphOutputStore` (share-URL refs) swaps in behind the same protocol only when a
   board-linkable URL is actually needed; that is why the seam's return type is `Path | str`
   (mirroring `RenderResult.ref`).

2. **`artifact` accepts bytes *or* a path.** A renderer already writes to a scratch path, so the
   common case is "file this rendered file durably" (copy, not move — the scratch `output/` is
   gitignored and fine to leave for inspection). Raw bytes are supported for callers that hold
   them in memory (and then a `name` is required — you can't infer a filename from bytes).

3. **The store is pure — it does not touch the board.** `put` files bytes and returns a `ref`;
   registering that `ref` back onto the board is the **gate ritual's** job (the next piece),
   exactly as `0005` separated "output bytes" from "pointer registered into the plan." Same
   discipline as keeping the Renderer ignorant of the ProductionProvider.

4. **`production / layer / name` key, `layer` left generic.** `0005` said `layer` = department;
   `0036` organizes deliverables by phase. Rather than commit, `layer` is a free string the
   caller chooses (`"plan"`, `"shoot"`, or a department) — the key shape is fixed, its meaning
   stays the caller's to decide until the gate ritual pins it down.

## Resulting state

- The data plane exists. `sequitur/output.py` gives the studio a durable, backend-swappable
  home for rendered bytes, keyed per production, reachable through a Protocol just like the
  render and production seams. `OUTPUT_STORE_ROOT` (OneDrive) makes the one shipped backend
  durable today. No new dependency (`shutil` + `pathlib`); 45 tests green; nothing else changed.

## Open threads

- **The gate ritual (next).** A small `Deliverable` concept + a per-phase review point: a phase
  emits an artifact → `OutputStore.put` → link the `ref` on the board (a State transition);
  revise re-opens and re-runs *that* phase. This is the piece that consumes `put`'s `ref`.
- **Wire the execute-hook → store.** `Director.execute` (`0032`) renders to a path; feed that
  `RenderResult.ref` into `OutputStore.put(production=…, layer=phase)` to close render → durable.
- Unchanged from `0036`/`0037`: the **Screenwriter treatment** (Directing Ch. 3–11), the
  **Production Designer seat + key-art source**, and binding the production **selector** into
  the Director / dailies loop. Then the first slice — **plan → {treatment + poster} → gate**.
- Later: `GraphOutputStore` (SharePoint share-URL refs via Microsoft Graph) behind the same
  protocol, when the board needs a hyperlink rather than a local path.
