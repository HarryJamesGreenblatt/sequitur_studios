# Chapter 3 — Visual History

> Abridged from Michael Rizzo, *The Art Direction Handbook for Film & Television* (2nd ed., Routledge/Focal Press), Ch. 3.
> **Scope:** the *media-technology* history of the moving image — how apparent motion, the split between film and video, the optical-toy origins of cinema, and the television-programming era each leave a **look** and a **vocabulary** an image prompt can name. Rizzo's "Visual History" is a history of the *medium*, not of art movements; the design-language it yields is medium/era/format and **genre** vocabulary, not a period-palette taxonomy.

## What this chapter actually is (and a caveat)

Rizzo's "Visual History" traces *how the moving image came to move*, not *how paintings looked in each century*. It debunks **persistence of vision** (the eye is not a video camera — there is no frame rate in the eye, only combined **motion**, **detail**, and **pattern** detectors) and then narrates two parallel lineages — television and film — from nineteenth-century tinkering to WebTV. For a generative image backend the payload is therefore **medium look**, **era markers**, and the **genre taxonomy** — not the art-historical periods a naive reading of the title expects. The richer palette-and-period vocabulary lives elsewhere: the [Colorist's `Look` library](../../../sequitur/crew/colorist.py) and the [Color Correction Handbook](../../color%20correction%20handbook/reference/ch04-primary-color-adjustments.md).

## Two media, two looks

The chapter's most usable distinction is that **film and video are physically different images**, and that difference *is* a look. **Telecine** (the **2:3 pulldown** that maps 24 film frames onto 29.97 video fields) exists only because the two rates don't align — and the seams of that mismatch are visible era markers.

| Axis | Film look | Video / TV look |
|---|---|---|
| Frame rate | 24 fps (film cadence; motion-blur, shutter flicker) | 29.97 fps, interlaced **fields** (telecine judder, scanlines) |
| Surface | grain, tinted film base, latitude | CRT phosphor glow, line structure, lower latitude |
| Origin | projected, cinematic | broadcast, "always on," small-screen |
| Aspect | wide (up to 2.7:1 Ultra Panavision, foreseen as early as du Maurier's 1879 cartoon) | historically 4:3 / 525-line NTSC |

A prompt that wants "1970s TV drama" is asking for the *video* column (interlaced, CRT-soft, 4:3); one that wants "70mm epic" is asking for the *film* column (grain, wide, projected).

## Era / origin markers

The technology timeline is itself a bank of **look references** — each stage carries an unmistakable aesthetic.

| Era marker | Vocabulary an image prompt can use |
|---|---|
| **Optical toys** (thaumatrope, phenakistoscope, zoetrope, praxinoscope, mutoscope, electrotachyscope) | hand-cranked, looping, illustrated-animation, parlor-novelty |
| **Early cinema** (Edison **kinetograph/kinetoscope**; Lumière **cinématographe**; **chronophotography** — Muybridge, Marey) | silent, sepia/tinted, flicker, black-flocked studio, motion-study strips |
| **Mechanical TV** (Nipkow disk, Baird's 30-line Televisor) | crude low-line raster, monochrome, ghosting |
| **Electronic TV** (Farnsworth Image Dissector, Zworykin Iconoscope/Kinescope, CRT) | broadcast black-and-white → NTSC color, scanlines |
| **WebTV / vodcast** | small-screen, compressed, short-form, handheld |

These are **camera obscura → chronophotography → CRT → LCD** waypoints; naming one places an image in its period without any art-movement label.

## Genre as design-language vocabulary

The single richest usable taxonomy in the chapter is Rizzo's **genre** list (distinct from **format**, which is the licensed program concept). Genres are "conventions that change over time" — exactly the open, extensible tag-set an image prompt draws on. Grouped:

| Family | Genres (Rizzo's list) |
|---|---|
| Drama forms | courtroom / legal / medical drama, docudrama, **dramality**, serial (episodic), soap opera, telenovela, anthology |
| Comedy / light | sitcom, variety show, stand-up, game show |
| Genre fiction | action, adventure, fantasy, sci-fi, western, **space western** |
| Factual / nonfiction | documentary, **mockumentary**, news, reality, educational, public broadcasting, religious, sports, infomercial |
| Animation / arts | animated cartoon, children's, art television, music |

This list maps directly onto the studio's [`Screenwriter` descriptor](../../../sequitur/crew/screenwriting.py) axes — `Supergenre` / `Macrogenre` and the **open-tag** `Microgenre` — the machine-readable classification the image prompt reads to set convention.

## Television as the forge of pop culture

Rizzo frames television, via semiotics, as *the* engine of the shared image — the **meme** (a unit of cultural transmission) that spreads by imitation. For the studio this is the rationale for treating genre/era markers as *recognizable* vocabulary: the audience already carries the visual conventions, so naming "film noir" or "1990s sitcom" in a prompt invokes a whole learned look. (**Nielsen** ratings/**share** and WebTV distribution are business context, not design vocabulary — omitted here.)

## Studio application

- **The genre list is the human-readable face of the [`Screenwriter` descriptor](../../../sequitur/crew/screenwriting.py).** Rizzo's genres populate the descriptor's `Supergenre`/`Macrogenre`/open-tag `Microgenre`; that classification is what the [`build_prompt`](../../../sequitur/prompt.py) pass turns into convention tokens for the [`ImageStudio`](../../../sequitur/image.py) backend. The planned **Production Designer** seat curates *which* markers a production leans on.
- **Medium/era markers are literal prompt tokens.** "Film grain, 2.35:1, projected" vs. "interlaced CRT, 4:3, scanlines" vs. "silent-era sepia, hand-cranked" are the era column the seat injects on top of the [`Director`'s `Brief`](../../../sequitur/crew/director.py) (scene + mood) before [`build_prompt`](../../../sequitur/prompt.py) renders a [`Shot`](../../../sequitur/shot.py).
- **Genre + era, not art-period, is where this chapter grounds the seat.** The seat's palette/period *execution* vocabulary comes from the [Colorist `Look`/`Cast`/`TonalRange` enums](../../../sequitur/crew/colorist.py) and the grade op basis in [`grade.py`](../../../sequitur/grade.py); Ch. 3 supplies the *conventions* those looks decorate.
- **Recognizability is the point.** Because a genre/era is a shared **meme**, one token ("noir," "spaghetti western," "'80s music video") carries a whole learned look into the prompt — cheap, dense design intent for a planned seat over [image.py](../../../sequitur/image.py).

> **Overlap flag:** Rizzo Ch. 3 supplies the **design intent** — the era/genre *concept* named in the image prompt ("warm 1970s film stock," "cold clinical broadcast video"). Van Hurkman supplies the **grade execution** — how that concept is realised as a color balance in [`grade.py`](../../../sequitur/grade.py). Keep them separate: name the palette *concept* here ([Color Correction Handbook Ch. 4 — Primary Color Adjustments](../../color%20correction%20handbook/reference/ch04-primary-color-adjustments.md) is the execution counterpart), and let the Colorist grade it downstream ([storyline 0020](../../../context/storyline/0020-grounding-color-the-colorists-handbook.md)).

Next: [Ch. 4 — The Design Process](ch04-the-design-process.md) — how a script becomes a **visual concept** and then a buildable design; the spine of the Production Designer seat.
