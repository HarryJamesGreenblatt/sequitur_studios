# Sequitur Studios

A generative **film studio** built on the Gemini **Omni Flash** video model. The
premise isn't "prompt a video model" — it's to model a *real production studio*:
the crew **roles** and **departments** of a film production (after Bowen's
Appendix D), working across the production **phases**, each grounded in proper
film-craft domain knowledge instead of vague prompts.

The studio has two halves, both taking shape:

- **A crew that decides.** Roles are first-class objects — a `Cinematographer`,
  `Gaffer`, and `KeyGrip` each *own* a slice of the shot grammar and *choose* their
  own values; a `Director` reconciles their proposals into a single, complete `Shot`;
  a dumb `Engine` dispatches a phase. Each role delegates its reasoning to a swappable
  `Judgment` (a deterministic **heuristic** today, an LLM **persona** or a **human**
  tomorrow), so any one seat can be upgraded — or hand-driven — on its own. The
  human is the **Producer** (brief, greenlight, approve); the agent crew executes.
- **A grammar that renders anywhere.** One model-agnostic grammar drives **three
  swappable backends**: **video** (Gemini Omni Flash), **still image** (Azure Foundry
  `gpt-image-1` — the Production Designer's look-dev deliverable), and **voice**
  (Azure AI Speech text-to-speech).

Today the studio fully implements the **camera department during production** —
grounded in Christopher J. Bowen's *Grammar of the Shot* and encoded as the typed
grammar under `sequitur/crew/`. The **grounding library spans every department the
architecture models**: seven film-craft sources imported and abridged — Bowen's *Grammar
of the Shot* and *Grammar of the Edit*, Jay Rose's *Producing Great Sound for Film and
Video*, Eric R. Williams' *The Screenwriter's Taxonomy*, Rabiger & Hurbis-Cherrier's
*Directing: Film Techniques and Aesthetics* (a Director-centric spine across every
phase), Paez & Jew's *Professional Storyboarding* (previsualization — a storyboard
panel *is* a pre-rendered shot), and Alexis Van Hurkman's *Color Correction Handbook*
(the grade — grounding a future Colorist). The remaining work is largely **code** —
building out the crew engine's other phases and roles. The full map lives in
[`context/architecture.md`](context/architecture.md).

## Setup

```powershell
# 1. Install dependencies
pip install -r requirements.txt

# 2. Sign in to Azure (secrets are fetched from Key Vault, not stored on disk)
az login

# 3. Point the studio at your resources (non-secret config only)
Copy-Item .env.example .env
#    then edit .env: set KEY_VAULT_NAME and your AZURE_OPENAI_IMAGE_ENDPOINT.
#    The API keys themselves live in Key Vault (secrets `gemini-api-key`,
#    `azure-openai-image-key`) and are read at runtime via your az-login identity.
#    The voice backend reuses the same Azure AI Services account (no new secret);
#    set AZURE_SPEECH_REGION in .env if it differs from the default.
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

Render a **still** instead of video (same grammar, image backend) with `--image`:

```powershell
# Composition, angle, lighting and colour transfer unchanged; motion, speed and
# sound are dropped. Saves to output/still_*.png.
python scripts/generate.py "an old fisherman mending nets on a weathered dock" `
    --size mcu --view three-quarter-front --angle low `
    --scheme low-key --quality soft --color-temp golden-hour `
    --mood "weathered, resolute" --image
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

### Let the crew compose the shot

Instead of specifying every grammar field yourself, hand the `Engine` a `Brief` and
let each role *choose* its own slice — the `Cinematographer` picks size/angle/lens,
the `Gaffer` the lighting, the `KeyGrip` the movement — and the `Director` reconciles
them into one complete `Shot`. Producer-level `hints` override any role's default:

```python
from sequitur import Engine, Brief, Phase, ShotSize, build_prompt

shot = Engine().run(
    Phase.SHOOT,
    Brief(
        scene="a detective studies a rain-streaked window at night",
        mood="tense, watchful",
        hints={"size": ShotSize.CLOSE_UP},   # the Producer overriding one default
    ),
)
print(build_prompt(shot))
```

Each role's reasoning is a swappable `Judgment` — deterministic (`HeuristicJudgment`)
today, an LLM `PersonaJudgment` over that role's grounded reference library, or a
`HumanJudgment`, later — so the crew can be upgraded seat by seat.

## Architecture — a production studio in layers

Design principle: each department/role owns a responsibility; every responsibility
is served by a **grounding source** (in the [grounding library](artifacts/INDEX.md))
and a **code layer** (in `sequitur/`). A user steps into a role and the workflow
hands them that role's grounded vocabulary and tooling.

| Phase | Departments (Bowen App. D) | Grounding source | Status |
|-------|----------------------------|------------------|--------|
| Pre-production | Producer · Screenwriter · Director · AD · Production Designer · Storyboard Artist | **The Screenwriter's Taxonomy** (story) + **Directing** (dramaturgy, aesthetics, design) + **Professional Storyboarding** (previs) — abridged | grounded; roles next |
| **Production** | **Camera · Electric · Grip** (+ Sound) | **Grammar of the Shot** — encoded under `crew/` | **implemented** |
| Post-production | Editor · Colorist · Sound editor · Composer | **Grammar of the Edit** + **Rose, *Producing Great Sound*** + **Color Correction Handbook** (Van Hurkman) + **Directing** Ch. 30–36 — abridged | grounded; `Editor` seated, code in progress |
| Delivery | Producer (marketing, distribution) | **Directing** Ch. 37 — abridged | grounded; out of code scope (for now) |

The studio's executable core is the **crew engine**: roles as behaviour (`Role` +
swappable `Judgment`), three authority tiers — **Producer = the human**,
**Director = the reconciling agent**, **Crew = the role components** — and the
**Production** (a plan whose buckets are these department layers) as the dumb
container. The full role → department → grounding → code-layer mapping, the runtime
model, and the diagrams are in [`context/architecture.md`](context/architecture.md).

## Layout

```
sequitur/      the studio code
  crew/        the crew engine — roles as behaviour, not just vocabulary
    role.py        Role base + Department/Phase axes + Brief/Contribution
    camera.py      Cinematographer — owns ShotSize/Angle/View/Lens/DoF/Composition
    lighting.py    Gaffer — owns LightQuality/Scheme/Direction/ColorTemperature
    grip.py        KeyGrip — owns CameraMovement/MotionSpeed
    editorial.py   Editor — owns Transition/EditReason/EditCategory
    judgment.py    swappable reasoning (HeuristicJudgment A · Persona B · Human)
    director.py    Director — reconciles crew Contributions into one Shot
    engine.py      dumb dispatch — Engine().run(phase, brief) -> Shot
  shot.py      the Shot aggregate the camera/electric/grip crews compose
  prompt.py    Shot -> film-literate prompt (build_prompt video / build_image_prompt still)
  studio.py    video render() / edit() over the Gemini Omni Interactions API
  image.py     still-image render() over Azure Foundry gpt-image
  speech.py    text-to-speech render() over Azure AI Speech (dry 48kHz/16-bit/mono)
  render.py    the renderer seam — Renderer protocol · Medium · renderer_for registry
  edit.py      post/editorial EDL + assembly model (Clip/Beat/Scene/Act/Sequence)
  cutter.py    MoviePy executor for the edit model
  config.py    .env pointers + Key Vault secret fetch (DefaultAzureCredential)
scripts/
  generate.py  CLI renderer (--image for stills, --dry-run to preview the prompt)
tests/         behaviour-guard tests (test_prompt · test_edit · test_engine · test_render)
artifacts/     grounding library — one folder per source (see INDEX.md)
  grammar of the shot/     production — cinematography (encoded under crew/)
  grammar of the edit/     post — editorial (grounds edit.py + the Editor)
  producing great sound.../ sound department (Jay Rose, 18 ch)
  the screenwriter's taxonomy/  development — genre/voice/pathway/POV (Williams, 8 ch)
  directing/               Director spine across every phase (Rabiger, 28 ch)
  professional storyboarding/  previs — staging/board types/workflow (Paez & Jew, 10 ch)
  color correction handbook/   post — color grading (Van Hurkman, 10 ch)
    reference/ abridged, session-ready references (ships)
    source/    verbatim ground truth (gitignored)
context/
  architecture.md   the production-studio layer map (roles -> grounding -> code)
  storyline/        project devlog (OVERVIEW.md + dated entries)
output/        generated clips (gitignored)
```

## Roadmap (by layer)

Grounding is complete for every department the architecture models; the remaining
work is **code**.

- **Crew engine — the next phases.** The shoot phase composes a `Shot` today
  (`Engine().run(Phase.SHOOT, Brief(...))`). Next: the **assemble** phase — the
  `Editor` chaining shots into a `Sequence` (honouring the 180°/30° rules,
  matching/reverse, eye-line, and screen direction; Ch. 5 of *Grammar of the Shot* is
  effectively its spec) — and binding a real **Production** (the PM board) in place of
  a bare `Brief`, through the `ProductionProvider`/`OutputStore` seams.
- **The `Screenwriter` role** — `crew/screenwriting.py` with the typed
  genre/voice/pathway/POV vocabulary the abridged *Screenwriter's Taxonomy* grounds;
  its contribution seeds the `Brief` the `Director` reconciles.
- **A Director persona** — swap the `Director`'s heuristic for a `PersonaJudgment`
  grounded in the abridged *Directing* chapters (the **B** in the A→B seam).
- **Sound & score** — `SpeechRenderer` (Azure Speech) is **built**; next are the
  `Composer`/`SoundAnalyst` roles over the
  [toaster-strudel](https://github.com/HarryJamesGreenblatt/toaster-strudel) MCP seam,
  and a formal `Renderer` protocol now that a third backend exists.
- **The casting/actors dimension** — a new layer *Directing* Ch. 18–20 grounds but no
  code models yet: a `Casting` role + a playable-intent performance concept wired to
  the image (character keyframes) and voice backends.
- **Reference-keyframe pipeline** — now grounded by the abridged *Professional
  Storyboarding* (a board panel *is* a reference keyframe): the `gpt-image` still
  backend already lands concept frames; next is a `StoryboardArtist` role that emits a
  per-shot keyframe and feeds it into `Studio.render` as a conditioning reference so the
  shot inherits its composition (image-to-video).

## Model note

Video is built on `gemini-omni-flash-preview` (native multimodal, conversational
editing); Veo 3.1 remains available for scene-extension and last-frame control.
Stills are rendered on an Azure Foundry `gpt-image-1` deployment, and voice on Azure
AI Speech — the first non-Google backends, proving the grammar is model-agnostic and
the renderer is a swappable seam. Backend API keys are never stored in plaintext:
they live in Azure Key Vault and are fetched at runtime via `DefaultAzureCredential`.

## License

MIT — see [`LICENSE`](LICENSE).

The `reference/` materials are original abridgements that summarise concepts from
their source works — Christopher J. Bowen's *Grammar of the Shot* and *Grammar of
the Edit* (4th eds.), Jay Rose's *Producing Great Sound for Film and Video* (4th ed.),
Eric R. Williams' *The Screenwriter's Taxonomy*, Michael Rabiger &
Mick Hurbis-Cherrier's *Directing: Film Techniques and Aesthetics* (6th ed.),
Sergio Paez & Anson Jew's *Professional Storyboarding: Rules of Thumb*, and
Alexis Van Hurkman's *Color Correction Handbook*; the
books' verbatim text is not distributed with this repository.
