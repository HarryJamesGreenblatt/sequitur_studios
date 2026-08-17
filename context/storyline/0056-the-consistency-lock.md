# 0056 — The consistency lock: conditioning renders on the cast reference

> Date: 2026-08-16 · Focus: **Casting Phase 3, step 1** — the execution mechanism the
> whole cast axis exists to enable. Give the still backend the ability to *condition* a
> render on the cast's locked reference images (the gpt-image **edits** endpoint), and let
> `Director.execute` forward those references. This is the consistency payoff: the same
> face carries across frames because the render is anchored to a real image, not a text
> description.

---

## What happened

Phase 2 (0055) produced a **locked reference** — every cast `Actor`'s audition keyframe,
filed durably. But a locked reference is inert until something *renders against it*. A text
prompt cannot guarantee identity (the memory's own lesson: for identity/spatial constraints,
a reference image beats prompt-only every time — the model reconstructs a plausible-but-
different person each call). So Phase 3 begins with the mechanism that consumes the lock.

1. **Conditioning is the edits endpoint, not a new renderer.** gpt-image generates from
   text via `images.generate`; it *conditions on an input image* via `images.edit`. So the
   still backend keeps one identity — `ImageStudio` — and simply routes to `edit` when
   references are present. Casting still makes a still; it rides the same producer (the 0019
   facilitative-renderer principle holds).

2. **`ImageStudio.render` gained `references`.** When given (paths to locked keyframes), the
   render opens them and calls the edits endpoint conditioned on those images; without them
   it takes the plain generation path unchanged. A small `_edit` helper opens the reference
   files under an `ExitStack` (deterministic close) and passes them as the `image` list.

3. **`ImageStudio` is now offline-constructible.** Added an injected-`client` path to
   `__init__` — pass a stub client (and config) and construction touches no endpoint,
   credential, or network. This is what makes the conditioning seam unit-testable, and it is
   generally useful (custom transports, tests).

4. **`Director.execute` forwards the references.** The hook gained an optional `references`
   list, forwarded to the backend **only when given** — so text-only media are untouched and
   the existing render path is byte-for-byte unchanged when no references flow. A greenlit
   Shot can now render conditioned on its cast: `Director.execute(shot, medium=STILL,
   references=[nora.cast.reference])`.

## Decisions

1. **Reuse `ImageStudio` + the edits endpoint; add no renderer.** The conditioning is a
   capability of the still producer, keyed by whether references are present.
2. **`references` is opt-in and pass-through.** `execute` forwards them only when non-`None`,
   so no existing caller or test changes behaviour; pairing references with a text-only
   medium is the caller's responsibility (the same no-policing stance the hook already takes).
3. **Client injection over monkeypatching.** A first-class `client=` argument is cleaner than
   reaching into internals and doubles as the offline-test seam.
4. **The automatic Shot→references join is the *next* step, not this one.** A Shot does not
   yet know which characters it features; wiring that (so `execute` derives references from
   the Shot's cast) is a real diegetic-join decision deferred to its own step. Today the
   references are an explicit argument — the honest seam.

## Resulting state

- **New code:** [`ImageStudio.render(..., references=…)`](../../sequitur/image.py) + the
  `_edit` helper + an injected-`client` constructor path;
  [`Director.execute(..., references=…)`](../../sequitur/crew/director.py) pass-through.
- **Tests:** [`test_render.py`](../../tests/test_render.py) 6 → 7 (an offline stub-client
  test: references route to `edit`, no references route to `generate`, and the reference
  file reaches the call); [`test_engine.py`](../../tests/test_engine.py) 10 → 11 (the
  execute hook forwards the locked reference to the backend). **12-module suite green.**
- The mechanism exists: a locked cast reference can now anchor a downstream still render.

## Next

- **The diegetic join:** let a Shot carry the characters it features so `Director.execute`
  derives the references automatically (the Shot ↔ cast-axis join) — and thread the cast look
  into `build_image_prompt` so text and reference agree.
- **Key art on the reference:** condition the KeyArtist's one-sheet on the protagonist's
  locked reference (the direct 0051 payoff — the protagonist not just *present* but *the same
  person*).
- **Graph references:** a `GraphOutputStore` ref is a URL, but the edits endpoint needs
  bytes; decide fetch-then-condition vs. keeping a local mirror for conditioning inputs.
- **Live proof:** run a real conditioned render through `gpt-image` (this session's proof was
  offline with a stub client) to confirm the identity actually carries.
