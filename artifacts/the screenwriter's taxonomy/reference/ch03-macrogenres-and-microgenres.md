# Chapter 3 — Macrogenres and Microgenres

> Abridged from Eric R. Williams, *The Screenwriter's Taxonomy*, Ch. 3.
> **Scope:** the two layers that add *specificity* beneath a supergenre — ~50
> **macrogenres** (interchangeable modifiers) and 200+ **microgenres** (macro-bound
> details) — and the rules for combining them.

## Core idea

Where a **supergenre** *defines* Story/Character/Atmosphere, a **macrogenre**
*refines* it. Macros like **Time Travel** or **Mystery** feel like they could be
genres, but alone they fix nothing ("it involves… time travel"). Their power is that
they are **interchangeable**: pair one with any supergenre and specific expectations
emerge, molded by the super already chosen.

- Time Travel × Crime = *Time Crimes*; × Romance = *The Time Traveler's Wife*;
  × Western = *Back to the Future III*.
- Mystery × Horror drives the *environment*; × Sports drives the *story*; × Western
  drives the *characters* to a final shootout.

## Macrogenres (~50, an open list)

Addiction, Adventure, Alien Invasion, Artificial Intelligence, Apocalyptic,
Biography, Bro-/Womance, Demonic, Disaster, Disease/Disability, Epic/Saga, Erotica,
Escape, Family, Gangs, Gangster, Ghost/Spirits, Heist/Caper, Historical, Holiday,
Identity, Killing, Law Enforcement, Legal, Love, Magical, Martial Arts, Medical,
Military, Mission, Monster, Mystery/Detective, Political, Procedural, Protection,
Psychological, Religious, Revenge/Justice, Romantic Comedy, Science Fantasy, School,
Showbiz, Slasher, Spy/Espionage, Superhero, Superpowers, Survival, Terror, Time
Travel, Workplace… (**not exhaustive** — the list is meant to grow).

**Macrogenre rules of thumb**

1. **Any macro can, in theory, pair with any super** — some pairings work better
   than others. Action/Thriller act like *adjectives* (more action-packed / more
   thrilling) and pair widely; Horror, Sports, and Western are the hardest to pair
   (their expectations overshadow the partner).
2. **You can attach more than one macro** (e.g. Crime + Addiction + Gangster =
   *Scarface*).
3. **Supergenres can serve as each other's macro** (Romance-as-macro over War =
   *Casablanca*; Sci-Fi with Romance-as-macro = *Eternal Sunshine*).

11 supers × 50 macros ≈ **550 combinations** before micros even enter.

## Microgenres (200+, macro-specific)

A **micro** is unique to its macro and adds the finest specificity without changing
the macro's expectations. The Addiction macro's micros: *Actions, Alcohol, Drugs,
Gambling* — each focuses the same macro differently (Gambling → economic ruin of the
family; Drugs → abuse of the protagonist's own mind/body).

**Microgenre rules of thumb**

1. Micros are **specific to their macro** (treat them as unique to it).
2. You can pair **more than one** micro with a macro.
3. There is **always at least one** micro per macro.

**The lever that multiplies stories:** keep a macro+micro fixed and *swap the
supergenre*. Drug-addiction **Crime** (*Drugstore Cowboy*) focuses on criminal acts;
drug-addiction **Day-in-the-Life** (*Permanent Midnight*) focuses on daily personal
ruin. Same details, different super, entirely different film. All told the taxonomy
offers ~55,000 configurations at this level alone.

## Studio application

- **Three tiers → three storage shapes.** `Supergenre` is a **closed enum** (Ch. 2);
  `Macrogenre` is a **large but curated enum** (interchangeable modifiers, multiple
  allowed); `Microgenre` is best modeled as an **open, macro-scoped tag** (200+ and
  meant to grow). This is exactly the closed-vs-open discipline the crew already
  practices — closed grammar enums for the DP, open free-text where the domain is
  genuinely unbounded.
- **Multiplicity is a first-class field, not a scalar.** A `Screenwriter`
  `Contribution` should carry **a list** of macros (each with ≥1 micro), mirroring how
  the model already merges *disjoint* department slices in the `Director` reconciler —
  here the slices are genre modifiers layered onto one supergenre.
- **The "swap the super, keep macro/micro" lever is a knob for variation.** For a
  studio that wants *varied* output from one seed idea, holding the macro/micro fixed
  and rolling the supergenre is a cheap, structured randomizer — the story-layer
  analogue of the "randomize per-cycle entry state to prevent a scripted feel" tactic
  used elsewhere in the studio's visual work.
- **Pairing-difficulty is domain knowledge worth encoding.** "Action/Thriller pair
  widely; Horror/Sports/Western resist" is a compatibility matrix a `PersonaJudgment`
  (the **B** seam) could consult to avoid proposing awkward super×macro combinations.

Worked examples of the full super/macro/micro delineation are in
[Ch. 4](ch04-genre-case-studies.md).
