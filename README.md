# Sequitur Studios

A generative **film studio** built on the Gemini **Omni Flash** video model. The
premise isn't "prompt a video model" — it's to model a *real production studio*:
the crew **roles** and **departments** of a film production (after Bowen's
Appendix D), working across the three production **phases**, each grounded in
proper film-craft domain knowledge instead of vague prompts.

Today the studio implements the **camera department during production** — grounded
in Christopher J. Bowen's *Grammar of the Shot* and encoded as the typed grammar in
`sequitur/grammar.py` — and renders that one grammar through **two swappable
backends**: **video** (Gemini Omni Flash) and **still image** (Azure Foundry
`gpt-image-1`, the Production Designer's look-dev deliverable). The **editorial/post**
and **sound** departments are already **grounded** — their reference libraries
imported and abridged (Bowen's *Grammar of the Edit* and Jay Rose's *Producing Great
Sound for Film and Video*) — with their code layers next to build. Every other
department and phase (pre-production, art, delivery) is scaffolded as the intended
architecture, ready to grow into. The full map lives in
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

## Architecture — a production studio in layers

Design principle: each department/role owns a responsibility; every responsibility
is served by a **grounding source** (in the [grounding library](artifacts/INDEX.md))
and a **code layer** (in `sequitur/`). A user steps into a role and the workflow
hands them that role's grounded vocabulary and tooling.

| Phase | Departments (Bowen App. D) | Grounding source | Status |
|-------|----------------------------|------------------|--------|
| Pre-production | Producer · Screenwriter · Director · AD · Production Designer | *(story / design — to acquire)* | partial (image look-dev) |
| **Production** | **Camera · Electric · Grip** (+ Sound) | **Grammar of the Shot** — encoded in `grammar.py` | **implemented** |
| Post-production | Editor · Colorist · Sound editor · Composer | **Grammar of the Edit** + **Rose, *Producing Great Sound*** — abridged | grounded; code next |
| Delivery | Producer (marketing, distribution) | — | out of scope (for now) |

The full role → department → grounding → code-layer mapping is
[`context/architecture.md`](context/architecture.md).

## Layout

```
sequitur/      the studio code
  grammar.py   Bowen's vocabulary as typed, orthogonal enums + the Shot dataclass
  prompt.py    Shot -> film-literate prompt (build_prompt video / build_image_prompt still)
  studio.py    video render() / edit() over the Gemini Omni Interactions API
  image.py     still-image render() over Azure Foundry gpt-image
  edit.py      post/editorial EDL + grammar model (Transition, Clip/Scene/Act)
  cutter.py    MoviePy executor for the edit model
  config.py    .env pointers + Key Vault secret fetch (DefaultAzureCredential)
scripts/
  generate.py  CLI renderer (--image for stills, --dry-run to preview the prompt)
artifacts/     grounding library — one folder per source (see INDEX.md)
  grammar of the shot/               production — cinematography (encoded in grammar.py)
  grammar of the edit/               post — editorial (grounds edit.py)
  producing great sound for film.../ sound department (Jay Rose, 18 ch)
    reference/ abridged, session-ready references (ships)
    source/    verbatim ground truth (gitignored)
context/
  architecture.md   the production-studio layer map (roles -> grounding -> code)
  storyline/        project devlog (OVERVIEW.md + dated entries)
output/        generated clips (gitignored)
```

## Roadmap (by layer)

- **Editorial / post** — *Grammar of the Edit* is imported and abridged; the
  `edit.py` model + `cutter.py` executor are scaffolded. Next: build the
  **cut-decision engine** and the **sequence** planner — chain shots into scenes
  honouring the 180°/30° rules, matching/reverse shots, eye-line, and screen
  direction (Ch. 5 of Grammar of the Shot is effectively its spec).
- **Sound** — designed as a multi-phase department and grounded by Jay Rose's
  *Producing Great Sound for Film and Video* (18 ch abridged); build
  `SpeechRenderer` (Azure Speech) first, then the `Composer`/`SoundAnalyst` roles
  over the [toaster-strudel](https://github.com/HarryJamesGreenblatt/toaster-strudel)
  MCP seam.
- **More departments** — story/screenwriting, production design, and colour are
  named in the [architecture](context/architecture.md) with no source yet; import
  each into the grounding library as the studio grows.
- **Reference-keyframe pipeline** — the `gpt-image` still backend already lands
  concept frames; next is feeding a still into `Studio.render` as a conditioning
  reference so the shot inherits its composition (image-to-video).

## Model note

Video is built on `gemini-omni-flash-preview` (native multimodal, conversational
editing); Veo 3.1 remains available for scene-extension and last-frame control.
Stills are rendered on an Azure Foundry `gpt-image-1` deployment — the first
non-Google backend, proving the grammar is model-agnostic and the renderer is a
swappable seam. Backend API keys are never stored in plaintext: they live in Azure
Key Vault and are fetched at runtime via `DefaultAzureCredential`.

## License

MIT — see [`LICENSE`](LICENSE).

The `reference/` materials are original abridgements that summarise concepts from
their source works — Christopher J. Bowen's *Grammar of the Shot* and *Grammar of
the Edit* (4th eds.) and Jay Rose's *Producing Great Sound for Film and Video*
(4th ed.); the books' verbatim text is not distributed with this repository.
