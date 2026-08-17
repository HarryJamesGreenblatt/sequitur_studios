# 0059 — Fork 3: the share-link store and fetch-then-condition

> Date: 2026-08-16 · Focus: resolve the 0057/0058 **fork 3** — make the Graph output store
> provide authoritative **share links** (as originally proposed, 0038/0053), and add the
> **fetch-then-condition** path so a render can seed on a durable share-URL reference, not
> just a local file. Closes the URL→bytes gap the cast-conditioning work opened.

---

## What happened

Two halves of one seam had drifted apart. `GraphOutputStore` (0053) already *uploaded* bytes
and returned an authoritative `webUrl`, but nothing let a production **select** it, and — the
sharper problem — a durable ref is now a **URL**, while the gpt-image edits endpoint needs
**bytes**. So the moment a locked cast reference lived in Graph (a share URL), conditioning
would break: `_edit` only knew how to `open()` a local path. Fork 3 closes both.

1. **The store is selectable.** `config.get_output_store()` returns the `GraphOutputStore`
   when `OUTPUT_STORE_BACKEND=graph` (with `GRAPH_DRIVE_ID` set), else the local folder — so a
   production's durable refs become authoritative **SharePoint share URLs** by config, no code
   change (the 0053 design, now reachable).

2. **The store can fetch back.** `OutputStore.fetch(ref) -> bytes` is a new protocol method —
   the store that *minted* a ref knows how to *resolve* it:
   - `LocalFolderOutputStore.fetch` reads the local path.
   - `GraphOutputStore.fetch` resolves a **share URL** through Graph's **shares** API: the URL
     is encoded to a share token (`u!` + unpadded base64url) and its `driveItem/content`
     downloaded. A plain local path (a mixed-store ref) is read directly.

3. **Fetch-then-condition.** A module helper `fetch_reference(ref, *, store=None)` resolves a
   reference — local path *or* share URL — to bytes: a URL goes through the configured store's
   `fetch`, a path is read directly. `ImageStudio._edit` now uses it: a URL reference is
   fetched to a `BytesIO` (named from the URL tail) and passed to the edits array; a local path
   is opened as before. So a render conditions on a durable share-link identity transparently.

## Decisions

1. **The store resolves its own refs.** URL→bytes is not the renderer's concern — the store
   that authenticates and downloads owns it (`fetch` on the seam). The renderer just asks
   `fetch_reference`, which delegates to the store for URLs.
2. **Graph's shares endpoint, not the content endpoint.** A `webUrl` is a browser/share link,
   not a content URL; the `shares/u!{token}/driveItem/content` route is the correct,
   auth'd way to turn a share URL back into bytes.
3. **Backend selection by explicit env flag.** `OUTPUT_STORE_BACKEND=graph` opts in
   deliberately (default stays local/OneDrive) — no silent behaviour change.
4. **Mixed refs tolerated.** Both `fetch` implementations read a plain path when the ref isn't
   a URL, so a store swap mid-production never strands an old local reference.

## Resulting state

- **Code:** `OutputStore.fetch` (protocol + both backends) + `GraphOutputStore._download`
  (shares endpoint) + `fetch_reference` ([`output.py`](../../sequitur/output.py));
  `config.get_output_store()` factory; `ImageStudio._edit` URL-aware
  ([`image.py`](../../sequitur/image.py)); `fetch_reference` exported.
- **Tests:** [`test_output.py`](../../tests/test_output.py) +7 (local/Graph fetch, mixed refs,
  `fetch_reference` local + URL-through-store, backend selection);
  [`test_render.py`](../../tests/test_render.py) +1 (a URL reference is fetched then
  conditioned). **12-module suite green.** Graph paths stubbed — no network.
- Fork 3 is closed in code: durable refs can be share URLs, and a render seeds on them.

## Next (the remaining resolved forks)

- **Wire the CLIs to `get_output_store()`** so `deliver_plan` / the Gate file through Graph when
  selected (the config exists; the plan producers still construct a store directly) — then a
  **live** run to confirm the share URL round-trips (upload → webUrl → shares fetch).
- **Omni video path** (fork 2): the multimodal `input` list + `previous_interaction_id`
  stateful thread, budget-aware to the ~4–5 character cap.
- **Overflow policy** (fork 4): surface a budget-exceeded cast to the Producer via the 0058
  approvals loop.
