# Chapter 2 — Movie Types and Supergenres

> Abridged from Eric R. Williams, *The Screenwriter's Taxonomy*, Ch. 2.
> **Scope:** the top two layers — **Type** (Comedy/Drama) and the **eleven
> supergenres** — plus the definition of what a "genre" actually *is*
> (Atmosphere · Character · Story). This is the taxonomy's densest **vocabulary**
> chapter and the strongest enum candidate.

## Layer 1 — Type: Comedy or Drama

The most basic split (the taxonomy's "kingdom"): a film is fundamentally **funny or
serious**. Each Type has *brands* — flavors, not genres:

- **10 brands of Drama:** Dark Drama, Docudrama, Docufiction, Dramedy, Hyperdrama,
  Light Drama, Satire, Straight Drama, Tragedy, Tragicomedy.
- **12 brands of Comedy:** Bathroom, Comedy of Ideas, Comedy of Manners, Dark/Black,
  Farce, Observational, Parody/Spoof, Sex Comedy, Situational, Straight, Slapstick,
  Surreal.

> **Beware false friends.** Some names *contain* "comedy"/"drama" but live elsewhere
> in the taxonomy: "Melodrama" and "Screwball Comedy" are **pathways**
> ([Ch. 6](ch06-pathway.md)); "Romantic Comedy" and "Family Drama" are **macrogenres**
> ([Ch. 3](ch03-macrogenres-and-microgenres.md)). A koala isn't a bear.

## What "genre" actually means — the three fundamentals

A true genre sets concrete audience expectations on **three axes**:

- **Atmosphere** — Location · Costumes & Props · Visceral expectations (what gets the
  heart racing).
- **Character** — Character types · their Goals · Stock characters.
- **Story** — Theme · Tentpole (expected) scenes · Story rhythm.

By this test, "Comedy," "Musical," "Kids' Movie" are *not* genres — they fix none of
Atmosphere/Character/Story (they only promise "funny," "singing," "no swearing").
Useful descriptors; not genres.

## Layer 2 — The eleven supergenres

Sixty-odd real genres collapse under **eleven umbrellas** that *define* the Story /
Character / Atmosphere everything else inherits:

**Action · Crime · Fantasy · Horror · Life · Romance · Science Fiction · Sports ·
Thriller · War · Western.**

Each carries a compact expectation bundle. The through-lines a writer must know:

| Supergenre | Core dichotomy / theme | Signature rhythm |
|------------|------------------------|------------------|
| **Action** | resourceful hero vs. single-minded villain; Good vs. Evil | internal ⇄ external problem alternate |
| **Crime** | Criminal vs. Lawman; truth/justice/freedom | Us vs. Them; double-cross |
| **Fantasy** | wonderment; personal (not societal) stakes | Hero's Journey; gather the band → epic confrontation |
| **Horror** | Sin vs. Purity; penance | group whittled by an unseen aggressor |
| **Life** (day-/slice-of) | we all share the same struggles | follow one protagonist, or ensemble parallel |
| **Romance** | love in its many axioms | Boy vs. Girl; pro-con-pro-con |
| **Science Fiction** | the unknown; social critique via metaphor | chameleon — borrows its macro's rhythm |
| **Sports** | Our Team vs. Their Team; underdog | cross-cut the two until the Big Game |
| **Thriller** | unwitting hero vs. epic villain; hope ⇄ fear | drop hero into a dark world, withhold the reveal |
| **War** | will to survive; sacrifice | group whittled (like Horror) or Us vs. Them (like Sports) |
| **Western** | law vs. chaos; taming the wild | protagonist peeled from society → final standoff |

Each supergenre in the book ships a full **Story / Character / Atmosphere** spec (themes,
expected scenes, story rhythm; character types + goals + stock characters; location,
costumes/props, visceral expectations) — the concrete expectation table a writer
works with or against.

## Studio application

- **This is the single most enum-shaped chapter in the source.** `MovieType`
  (`COMEDY | DRAMA`) is a two-value enum; `Supergenre` is a **closed 11-value enum** —
  the exact pattern that made `ShotSize`/`CameraAngle` in
  [`crew/camera.py`](../../../sequitur/crew/camera.py). A future `Screenwriter` role
  owns both.
- **A supergenre is a *bundle*, not a label — which is the payoff.** Because each
  super fixes Story/Character/Atmosphere, selecting one **seeds defaults across
  departments**: its *location/costume/visceral* expectations brief the
  Production Designer and DP; its *theme/rhythm* brief the Editor's pacing; its
  *character goals* brief casting/performance. This is the plan-phase analogue of how
  a `Shot`'s grammar seeds `build_prompt`.
- **Type-brands and drama/comedy-that-aren't map cleanly onto the model.** The
  "koala isn't a bear" warnings (Melodrama = pathway, Rom-Com = macro) are a
  reminder to keep the layers as **distinct fields**, not one flat tag — exactly why
  the crew keeps vocabulary in separate role-owned enums rather than a single blob.
- **Heuristic default:** absent a Producer brief, a Screenwriter heuristic could
  default `Type=DRAMA`, `Supergenre=LIFE` (the most "mundane/realistic" umbrella,
  cheapest to render) and let hints override — the same defaulting discipline the
  shoot roles already follow ([storyline 0014](../../../context/storyline/0014-the-crew-behaviour.md)).

Next: the [macro/micro layer](ch03-macrogenres-and-microgenres.md) that *refines* a
supergenre.
