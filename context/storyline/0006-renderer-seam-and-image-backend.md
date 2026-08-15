# 0006 — The renderer seam; a second (image) backend; secrets in Key Vault

> Date: 2026-08-08 · Focus: generalize "the engine renders video with Gemini" into
> a **renderer seam** with swappable backends, and prove it by adding a second,
> **non-Google** backend — still-image generation on **Azure Foundry `gpt-image-1`**.
> Also hardened credential handling: secrets moved out of `.env` into **Azure Key
> Vault**. Unlike `0005`, this one is **built, not just decided.**

## The problem

The studio was implicitly one model deep: "compose a grammar-grounded prompt, send
it to Gemini Omni." But the department architecture ([`architecture.md`](../architecture.md))
implies *heterogeneous deliverables* — a script is text, a look is a still, a shot
is video, an edit is a timeline, sound is audio — and each is best served by a
different model, source, or data API. Forcing every department through one video
model under-serves the others. The coupling to Gemini was thin (only `studio.py`
plus the video-shaped `build_prompt`), so the fix was a **seam**, not a rewrite.

Image generation was the right first case to prove it: still images are the
**Production Designer**'s native deliverable *and* — more usefully — a **reference
keyframe** the video studio can condition a shot on (text can't reliably pin
composition/orientation; a reference image can).

## Decisions

1. **Grammar is model-agnostic; only the *renderer* is backend-bound.** The Bowen
   vocabulary in [`grammar.py`](../../sequitur/grammar.py) knows nothing about any
   model. A **renderer** is the swappable thing that turns a `Shot` (seeds +
   guidance) into output. This is the third seam alongside `0005`'s
   `ProductionProvider` / `OutputStore`.

2. **A still is the video prompt minus the moving parts.** The image prompt reuses
   the shared composition logic and simply drops motion, speed, `single_scene`, and
   audio — so [`build_image_prompt`](../../sequitur/prompt.py) is `build_prompt`
   without the video-only faces, not a new vocabulary. Framing, angle, lighting,
   colour-temp, focal length, and DoF all transfer unchanged.

3. **Backend follows the deliverable's medium, and need not be Google.** The image
   backend is **Azure Foundry `gpt-image-1`** on the user's existing deployment
   (an existing AIServices account, eastus2) — the first non-Google renderer,
   proving the seam. (The same account also has **`sora`**, a future Azure-native
   *video* alternative to Omni — noted, not wired.)

4. **Secrets live in Azure Key Vault, never in plaintext.** Both API keys
   (the Gemini and Azure image keys) live in a project Key Vault.
   [`config.py`](../../sequitur/config.py) fetches them at
   runtime via `DefaultAzureCredential` — the `az login` identity authorises the
   *vault read*, so no key ever touches the repo, `.env`, or model context. `.env`
   holds only **non-secret pointers** (vault name, endpoint, deployment,
   api-version); an explicit env var still overrides a secret for CI/offline. This
   is the same least-privilege posture `0005` set for the Graph output store, applied
   to the data plane.

## Resulting state (built and verified)

- **Two render backends, one grammar.** [`Studio`](../../sequitur/studio.py) = video
  (Gemini Omni Flash); [`ImageStudio`](../../sequitur/image.py) = still image (Azure
  `gpt-image-1`). Both share the same `Shot` and expose the same
  `render() -> (result, saved_path)` contract.
- **CLI:** `scripts/generate.py --image` renders a still; the default path renders
  video. `--dry-run` still needs no backend deps (imports are lazy).
- **Both paths validated live end-to-end:** a `gpt-image-1` still and a 2.5 MB Omni
  clip, each rendered from the same fisherman `Shot`, with keys pulled from Key Vault.
- **Env:** a project [`.venv`](../../.venv) (Python 3.12) is the interpreter; deps add
  `openai`, `azure-identity`, `azure-keyvault-secrets`.

## Open threads

- **Wire the reference-keyframe flow** — let a `gpt-image-1` still be passed to
  `Studio.render` as a conditioning reference for the shot (the higher-leverage use
  of image gen), rather than the two backends running independently.
- **Formalize the renderer seam in code** — today there are two sibling classes with
  a matching `render()` shape; a small `Renderer` protocol (and a registry keyed by
  deliverable medium) is worth adding once a *third* backend appears, per the repo's
  "make it first-class only when a second/third case justifies it" discipline.
- **Non-generative backends** — the seam should also admit **data APIs** (licensing,
  colour/reference lookups) for departments whose deliverable isn't a model output.
- **`sora` as an alternate video backend** — available on the same account; a natural
  second video renderer to test the seam's swappability on the video side.
- Carried: build the `0005` provider seams; acquire *Grammar of the Edit*; the
  sequence layer; broader discipline sources; a `build_prompt` smoke test.
