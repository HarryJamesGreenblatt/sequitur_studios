# Sequitur Studios

A generative **film studio** built on the Gemini **Omni Flash** video model. The
premise isn't "prompt a video model" — it's to model a *real production studio*:
the crew **roles** and **departments** of a film production (after Bowen's
Appendix D), working across the three production **phases**, each grounded in
proper film-craft domain knowledge instead of vague prompts.

Today the studio implements **one department in one phase** — the **camera
department during production** — grounded in Christopher J. Bowen's *Grammar of
the Shot* and encoded as the typed grammar in `sequitur/grammar.py`. Every other
department and phase (pre-production, editorial/post, sound, art, delivery) is
scaffolded as the intended architecture, ready to grow into. The full map lives
in [`context/architecture.md`](context/architecture.md).

## Setup

```powershell
# 1. Install dependencies
pip install -r requirements.txt

# 2. Add your key (never committed)
Copy-Item .env.example .env
#    then edit .env and paste your Sequitur Studios Gemini key
```

## First render

```powershell
# Preview the composed prompt without spending a call:
python scripts/generate.py "an old fisherman mending nets on a weathered dock" `
    --size mcu --view three-quarter-front --angle low --move dolly-in `
    --scheme low-key --quality soft --color-temp golden-hour `
    --mood "weathered, resolute" --audio "gulls, distant surf, no dialogue" --dry-run

# Drop --dry-run to actually render to output/clip_*.mp4
```

From Python / a chat session:

```python
from sequitur import Studio, Shot, ShotSize, CameraMovement, LightScheme

studio = Studio()
shot = Shot(
    scene="a lone astronaut drifting past a cracked visor reflection of Earth",
    size=ShotSize.CLOSE_UP,
    movement=CameraMovement.DOLLY_OUT,
    light_scheme=LightScheme.LOW_KEY,
    mood="awe, isolation",
    audio="only breathing and a faint radio hiss, no music",
)
interaction, path = studio.render(shot)
print(path)

# Iterate conversationally (Omni Flash is stateful):
_, path2 = studio.edit(interaction.id, "Add a slow blink. Keep everything else the same.")
```

## Architecture — a production studio in layers

Design principle: each department/role owns a responsibility; every responsibility
is served by a **grounding source** (in the [grounding library](artifacts/INDEX.md))
and a **code layer** (in `sequitur/`). A user steps into a role and the workflow
hands them that role's grounded vocabulary and tooling.

| Phase | Departments (Bowen App. D) | Grounding source | Status |
|-------|----------------------------|------------------|--------|
| Pre-production | Producer · Screenwriter · Director · AD · Production Designer | *(story / design — to acquire)* | planned |
| **Production** | **Camera · Electric · Grip** (+ Sound) | **Grammar of the Shot** — encoded in `grammar.py` | **implemented** |
| Post-production | Editor · Colorist · Sound editor | *Grammar of the Edit* — to acquire | next layer |
| Delivery | Producer (marketing, distribution) | — | out of scope (for now) |

The full role → department → grounding → code-layer mapping is
[`context/architecture.md`](context/architecture.md).

## Layout

```
sequitur/      the studio code
  grammar.py   Bowen's vocabulary as typed, orthogonal enums + the Shot dataclass
  prompt.py    Shot -> film-literate Omni Flash prompt
  studio.py    render() / edit() over the Interactions API
  config.py    .env loading and key handling
scripts/
  generate.py  CLI renderer (supports --dry-run)
artifacts/     grounding library — one folder per source (see INDEX.md)
  grammar of the shot/
    reference/ abridged, session-ready references (ships)
    source/    verbatim ground truth (gitignored)
context/
  architecture.md   the production-studio layer map (roles -> grounding -> code)
  storyline/        project devlog (OVERVIEW.md + dated entries)
output/        generated clips (gitignored)
```

## Roadmap (by layer)

- **Editorial / post** — acquire Bowen's *Grammar of the Edit* to ground the edit
  layer, then build the **sequence** planner: chain shots into scenes honouring
  the 180°/30° rules, matching/reverse shots, eye-line, and screen direction
  (Ch. 5 of Grammar of the Shot is effectively its spec).
- **More departments** — sound, story/screenwriting, production design, and colour
  are named in the [architecture](context/architecture.md) with no source yet;
  import each into the grounding library as the studio grows.
- **Stills-first pipeline** — Nano Banana concept frames → image-to-video.

## Model note

Built on `gemini-omni-flash-preview` (the current default video model:
native multimodal, conversational editing). Veo 3.1 remains available for
scene-extension and last-frame control when those become useful.

## License

MIT — see [`LICENSE`](LICENSE).

The `reference/` materials are original abridgements that summarise concepts from
Christopher J. Bowen's *Grammar of the Shot* (4th ed.); the book's verbatim text
is not distributed with this repository.
