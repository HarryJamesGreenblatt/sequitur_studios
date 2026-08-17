# 0053 — The Graph output store: authoritative URLs, the publish race closed

> Date: 2026-08-16 · Focus: build the second `OutputStore` backend — **`GraphOutputStore`**
> — that uploads a produced artifact's bytes to SharePoint/OneDrive **directly over the
> Microsoft Graph API** and returns an **authoritative** share URL only after the upload
> completes. Closes the *publish race* named in `0051` and delivers `0038`'s deferred
> "URL later." **New backend behind the existing seam; no seam change, no new dependency.**

---

## What happened

`0051` found and named a real bug. The Tier-0 store (`LocalFolderOutputStore` pointed at a
OneDrive-synced folder) files bytes to disk and leans on the **desktop sync client** to
publish them. The AD then mints an https link (`config.store_url` maps the local path →
`OUTPUT_STORE_URL_BASE`) and posts it to the board *before* the client has finished
uploading — so the URL is correct the instant it's minted but briefly serves the **stale**
blob until the client catches up. A race between "the link is posted" and "the bytes are
published."

`0038` had already anticipated this: it made the seam's return type `Path | str` precisely
so a URL-returning backend could swap in behind the same protocol ("Path now, URL later").
This session builds that backend.

1. **`GraphOutputStore` — the same protocol, an authoritative ref.**
   [`output.py`](../../sequitur/output.py) gains a second backend that satisfies the same
   `OutputStore` protocol (`put(artifact, *, production, layer, name=None)`). It uploads the
   bytes to `drives/{drive_id}/root:/<production/layer/name>:/content` over Graph (a simple
   PUT; Graph creates parent folders) and returns the item's **`webUrl`** — which is
   authoritative the instant the upload returns, because *this* process did the upload rather
   than delegating to a sync client. No dependence on client timing; no race.
2. **Auth + transport reuse what's already here.** The credential is the caller's Entra
   identity (`DefaultAzureCredential` on the Graph `.default` scope) — the same
   `azure-identity` already used for Key Vault, **no new dependency** — and the transport is
   stdlib `urllib`, mirroring `production.py`. `__init__` touches no network (token and every
   request are lazy), so the store constructs safely offline and in tests.
3. **Config, non-secret and env-driven.** New `GraphStoreConfig` / `get_graph_store_config()`
   read `GRAPH_DRIVE_ID` (the target SharePoint document-library drive) and optional
   `GRAPH_STORE_ROOT_PATH` (a subfolder) from `.env` — both non-secret pointers, like every
   other store/board pointer. It fails loudly if the drive id is unset.

## Decisions

1. **A backend, not a seam change.** The whole point of the `0038` protocol was that a new
   durability tier is *additive*. `GraphOutputStore` adds no method, changes no signature; the
   only "asymmetry" (a `str` URL ref vs a `Path`) was designed in from the start.
2. **Return `webUrl` directly** rather than minting a link separately (as the local path +
   `store_url` dance does). The upload response *is* the authoritative reference — the URL and
   the bytes are published in the same call, which is exactly what dissolves the race.
3. **Keep the local backend.** Tier-0 (OneDrive-synced folder) stays the zero-config default;
   `GraphOutputStore` is the tier you point at when the eventual-consistency window matters
   (posting a board link the Producer will click immediately).

## Resulting state

- Two `OutputStore` backends behind one protocol: `LocalFolderOutputStore` (Tier-0, free
  durability, eventually-consistent link) and **`GraphOutputStore`** (authoritative URL,
  race-free). Exported from the package; `tests/test_output.py` covers the Graph backend's
  key construction + bytes-need-a-name guard via a stubbed upload (offline, no network).
- The full 11-module smoke suite is green.

## Next

- **Wire the Graph backend into a live run** — provision `GRAPH_DRIVE_ID` for the tenant's
  document library and file one real plan deliverable through it, confirming the board link is
  authoritative on first click.
- The verdict loop (`0052`) and `Cut` maturity states remain the open board threads.
