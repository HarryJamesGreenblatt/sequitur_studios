# 0057 — Conditioning mechanics: how the backends actually take a seed

> Date: 2026-08-16 · Focus: a **design memo (no code beyond step 1)** answering the
> Producer's question — *does the plan to "apply the cast to a shot" account for how Omni
> and gpt-image actually accept image/video seeds, and the contingencies of multiple
> characters and characters in specific conditions?* Verified both backends' ingestion
> models, named the procedural contingencies, and set the design for the Shot↔cast join.
> Ships the minimal fork-independent slice; the rest is staged.

---

## Why this memo

0056 gave `ImageStudio` a `references` argument and `Director.execute` a pass-through, then
proposed "thread the reference into the shot." The Producer rightly paused: the still path
(gpt-image **edits**) and the video path (**Omni**) accept seeds very differently, and a flat
`references=[...]` list ignores real contingencies — multiple characters and characters
depicted *in specific conditions*. This memo grounds the design in the **verified** APIs
before more plumbing hardens the wrong shape.

## What the backends actually do (verified)

**Still — Azure `gpt-image` (edits endpoint), what 0056 built:**
- `images.edit(model, image=[f1, f2, …], prompt, [mask])` — one *or more* reference images
  as an **array**. Confirmed against the OpenAI image guide (the 4-image gift-basket example).
- **No per-image role binding.** The model attaches references to subjects **only via the
  prompt** ("…containing all the items in the reference pictures"). There is no "this image
  = character A" channel.
- A **mask** (inpainting) applies to the **first** image only when several are passed.
- **`input_fidelity: high`** exists on `gpt-image-1` to preserve faces/features (automatic on
  `gpt-image-2`). A lever for holding a locked face.
- Documented limitation: the model "may occasionally struggle to maintain visual consistency
  for recurring characters … across multiple generations" and with "layout-sensitive
  compositions." So conditioning **helps but does not guarantee** identity.

**Video / image — Gemini Omni (Interactions API):**
- `input` is a **typed multimodal parts list**: `{type:text}`, `{type:image, data|uri,
  mime_type}`, `{type:video, uri, mime_type}` — **not** an `images.edit`-style array. Our
  `Studio.render` currently passes `input=<text>` only, so the **video backend ingests zero
  image seeds today**; the 0056 edits shape does not transfer to it.
- **Typed & budgeted references:** up to 14 total, but only ~**4–5 "character" images** for
  consistency (plus ~10 "object", ~3 "style"). Character count in one frame is **capped**.
- Binding is still **prompt-driven** (name/position each subject in the text).
- Omni is **stateful** — `previous_interaction_id` carries a subject across turns: a *second*
  consistency mechanism (establish once, continue) orthogonal to reference-image passing.

## The procedural contingencies (named)

1. **Multiple characters is capped and prompt-coupled.** Neither backend binds an image to a
   role structurally; you bind by **naming and placing** each person in the prompt. And Omni
   holds only ~4–5 character references. So (a) passing a bare `references` list is
   insufficient the moment there is more than one person — the prompt builder must name them;
   and (b) a shot's character-reference count must respect a **budget**.
2. **Conditional depiction splits in two.**
   - *State conditions* (wet, wounded, back-lit, at distance, from behind): keep **one** locked
     reference, drive the state in the prompt, lean on consistency + `input_fidelity`. Cheap.
     Note our 0055 reference is a neutral portrait — good for a **face lock**, but it should not
     over-constrain framing; the reference is an *identity* anchor, not a *composition* anchor.
   - *Identity-defining conditions* (young vs. old, pre/post-transformation, a disguise): these
     are **distinct embodiments of the same Character** and want their **own** locked reference.
     That implies a Character may hold **multiple** references keyed by aspect/era/state — and
     casting may audition/select more than one embodiment per role.
3. **The durable ref may be a URL, but edits needs bytes.** A `GraphOutputStore` ref (0053) is a
   `webUrl`; gpt-image edits wants file bytes and Gemini wants inline base64 or a Files-API
   `uri`. Conditioning inputs need a **fetch-then-condition** (or local-mirror) path the
   durable-ref abstraction does not yet cover.
4. **Backends condition differently** — so a single flat seam is wrong. gpt-image = edits array;
   Omni = typed multimodal `input` (+ optional stateful `previous_interaction_id`).

## The design (where this is going)

The Shot↔cast join is **not** `references: list[str]`. It is a **typed, budgeted,
prompt-coupled** cast-in-shot model:

- A **Shot carries which characters appear** (references to `Character`, not raw paths), so a
  backend can (a) pull each one's locked reference *and* the prompt can (b) **name** them for
  binding.
- Conditioning is **typed** (character / object / style) and **budget-aware** (respect Omni's
  ~4–5 character cap; degrade gracefully) — mapping cleanly onto Gemini's categories and onto
  gpt-image's flat array.
- The conditioning seam is **per-backend**: `ImageStudio` fills the edits array; `Studio` builds
  a multimodal `input` list (and may use `previous_interaction_id` for cross-shot continuity).
  Each backend owns *how it conditions on a Shot's cast* — the Director stays dumb.
- **Conditional depiction** is first-class: a `Character` can hold **multiple locked references**
  keyed by aspect/state (deferred — see forks).

## Open forks (Producer's call)

1. **Conditional depiction model:** one locked reference + prompt-driven state (simplest), or
   multiple references per `Character` keyed by aspect/era/state (richest, touches casting)?
2. **Omni consistency strategy:** reference-image budget vs. **stateful** `previous_interaction_id`
   establishing shots — or both, and when?
3. **URL→bytes:** fetch-then-condition on demand, or keep a local mirror of conditioning inputs?
4. **Budget overflow policy** when a scene has more principals than the character-ref cap: drop
   by billing, split coverage, or rely on prompt-only for the overflow?

## Shipped this session (step 1 — the fork-independent core)

The one part that is right regardless of the forks: **the Shot carries its cast, the prompt
names them, and the still backend conditions on their locked references automatically.**

- `Shot.cast: list[Character]` (the diegetic join — which characters are in frame) +
  `Shot.locked_references()` (the cast Actors' locked keyframes).
- `build_prompt` / `build_image_prompt` append a **"Featuring …"** clause naming each cast
  member (and their look/essence) so a reference can bind to a name (prompt-coupled binding),
  for both video and still.
- `ImageStudio.render` derives references from a `Shot`'s cast when none are passed explicitly —
  the backend owns its conditioning (Director stays dumb). Explicit `references` still override.
- Tests: prompt naming, `Shot.locked_references`, and the still backend deriving+conditioning
  from a Shot's cast (offline stub client). Suite green.

## Next

- The **per-backend video path**: teach `Studio` the multimodal `input` list (+ decide the
  `previous_interaction_id` strategy) — the fork-2 decision.
- The **typed/budgeted** reference model (character/object/style, ~4–5 cap) once video lands.
- **Conditional depiction** (fork 1) + **URL→bytes** (fork 3) + **overflow policy** (fork 4).
- **Live proof:** a real conditioned still of a cast character in a scene (offline stubs only so far).
