# 0048 — The KeyArtist: the first Skill-encapsulated seat; and who owns the copy

> Date: 2026-08-16 · Focus: build the **KeyArtist** — a theatrical one-sheet (key art)
> producer — *not* as a `crew/` Role but as a **Skill** (`.github/skills/keyartist/`), the
> first **generalist-under-direction** seat. Plus the empirical finding on **who owns the
> marketing copy**. **Skill + composer code; no new crew module.**

---

## What happened

The plan phase produced *production art* (the PD's concept as a scene of the world), but a
theatrical **poster** — **key art** with a title treatment and tagline — is a different
discipline: graphic design / marketing, not production design. Rizzo's Ch. 1 split already
names it (production design ≠ key art). This session builds that seat, and it forces two
architectural firsts.

1. **No tenth source.** The nine grounded sources encode *specialist closed vocabularies*
   the model lacks. Poster design (hierarchy, negative space, type) is **general
   competence a frontier model already has** — a mediocre design primer would be
   pattern-worship. So the KeyArtist grounds on **nothing but inherited direction** (the
   PD's concept + the story's copy) and general competence.

2. **The KeyArtist as a Skill, not a Role.** Because it owns no source and no closed enum
   vocabulary, it doesn't fit the `abridge → crew/*.py Role + .agent.md` mould. It lives as
   **[`.github/skills/keyartist/SKILL.md`](../../.github/skills/keyartist/SKILL.md)** (the
   persona, tier B) + a bundled arm
   **[`compose_key_art.py`](../../.github/skills/keyartist/compose_key_art.py)** + a
   deterministic composer **`build_key_art_prompt`** in
   [`prompt.py`](../../sequitur/prompt.py) (tier A). This is the **first
   generalist-under-direction seat** — its brief is *another seat's output*, not a
   grounding.

3. **Invocation pattern (a), proven live.** A subagent reads the `SKILL.md`, reasons under
   the inherited direction, and returns a key-art directive (archetype, type placement,
   which motifs to foreground); the tool-holder runs the arm to render + file. Judgment in
   the subagent, execution in the terminal-holder — the same split every seat uses. The
   KeyArtist chose a hero-object archetype, foregrounded the right motifs, and pruned the
   clutter with stated reasons — a generalist executing cleanly under two parents.

4. **Type is generative (2026).** Empirically `gpt-image` renders **headline** type (title,
   tagline) legibly and correctly; it garbles **fine print** (billing block). So
   `build_key_art_prompt` quotes the title/tagline for exact spelling and leaves the
   billing block **off by default** — no compositing pipeline needed for the headline.

## Decision — who owns the marketing copy

The KeyArtist first authored its own tagline ("EVERY EMPTY CHAIR, A NAME") — **descriptive**
(it restated the visible motif), the same failure family as the tier-A treatment that
dumped taxonomy metadata as prose. Dispatching the **Screenwriter** to author the copy
theme-first produced "HE PAID FOR EVERY NOTE WITH SOMEONE HE LOVED" — **thematic**, welded
to the story's spine. Same image, same composer; only the copy owner changed, and the
poster went from competent to affecting.

- **Copy (title + tagline) → the Screenwriter.** It's one-line *thematic compression*
  ("aim at the heart"), reasoned from the story, not the frame.
- **Composition + look → the KeyArtist.** It *houses* the inherited copy (Screenwriter) and
  concept (PD); it never authors story or copy. **Its two parents are the PD (look) and the
  Screenwriter (words).** "Closest agent to the call" was the wrong default.

## Resulting state

- **Two Skills-pattern seats now** (KeyArtist here, AD/PA in `0049`) — the pattern the
  Skills reframe predicted, applied only where a seat is a generalist under direction, not
  a grounded specialist. No broad refactor of the nine grounded seats.
- The one-sheet renders live end-to-end (concept + copy → composer → `ImageStudio`), filed
  through a `Gate`.

## Next

- Copy authoring should move into the Screenwriter as a **derived step** (`descriptor →
  treatment → title/tagline`) so the tagline compresses an *authored* story, not a vacuum —
  and the KeyArtist should require inherited copy rather than being able to invent it.
