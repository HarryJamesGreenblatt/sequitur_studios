"""Compose a :class:`~sequitur.shot.Shot` into a well-formed model prompt.

Two renderers, two builders sharing one grammar:

- :func:`build_prompt` targets Gemini Omni Flash **video** — lead with the
  scene, layer camera and lighting language, describe sound design explicitly,
  enforce a single continuous shot when asked, fold negatives inline.
- :func:`build_image_prompt` targets a **still-image** backend (Azure Foundry
  ``gpt-image``) — the same framing, camera, and lighting grammar, minus the
  moving parts (movement, speed, audio, scene continuity).
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING

from .shot import Shot

if TYPE_CHECKING:
    from .cast import Actor, Character
    from .plan import Plan


def _compose(shot: Shot, *, moving: bool) -> str:
    parts: list[str] = []

    if shot.timing and moving:
        parts.append(shot.timing)

    # Core scene, optionally prefixed with the shot size for framing.
    if shot.size:
        parts.append(f"A {shot.size.phrase} of {shot.scene.rstrip('.')}.")
    else:
        parts.append(shot.scene.rstrip(".") + ".")

    # How the subject sits in the frame.
    framing = [f.phrase for f in (shot.view, shot.style, shot.composition) if f]
    if framing:
        parts.append("Framing: " + ", ".join(framing) + ".")

    # Camera: angle, lens / focus, and (video only) movement and speed.
    camera_fields = [shot.angle]
    if moving:
        camera_fields += [shot.movement, shot.speed]
    camera_fields += [shot.focal_length, shot.depth_of_field]
    camera = [f.phrase for f in camera_fields if f]
    if shot.lens:
        camera.append(shot.lens)
    if camera:
        parts.append("Camera: " + ", ".join(camera) + ".")

    # Lighting, composed from its orthogonal axes.
    light = [
        f.phrase
        for f in (
            shot.light_scheme,
            shot.light_quality,
            shot.light_direction,
            shot.color_temp,
        )
        if f
    ]
    if shot.eye_light:
        light.append("a catch light glinting in the eyes")
    if light:
        parts.append("Lighting: " + ", ".join(light) + ".")

    if shot.mood:
        parts.append("Mood: " + shot.mood.rstrip(".") + ".")

    if moving:
        # Omni Flash generates and syncs its own audio; be explicit to control it.
        if shot.audio:
            parts.append("Sound design: " + shot.audio.rstrip(".") + ".")
        if shot.single_scene:
            parts.append("A single continuous shot, no scene cuts.")

    if shot.avoid:
        parts.append("Do not include: " + ", ".join(shot.avoid) + ".")

    return " ".join(parts)


def build_prompt(shot: Shot) -> str:
    """Compose a Shot into a Gemini Omni Flash video prompt."""
    return _compose(shot, moving=True)


def build_image_prompt(shot: Shot) -> str:
    """Compose a Shot into a still-image prompt (framing/camera/lighting only)."""
    return _compose(shot, moving=False)


def build_poster_prompt(plan: "Plan") -> str:
    """Compose a :class:`~sequitur.plan.Plan`'s design half into a poster prompt.

    The poster is "the Production Designer's look as one evocative frame" (storyline
    0041/0046): the ``visual_concept`` is the spine, the medium/era/set and stance are
    look tokens, the motifs seed the frame. Unlike :func:`build_image_prompt` this reads
    the *design descriptor*, not a camera :class:`Shot`. When the concept is blank (the
    heuristic tier leaves it for the persona), it falls back to the scene.
    """
    d = plan.design
    concept = str(d.get("visual_concept") or "").strip()
    subject = (concept or plan.scene).rstrip(".")
    parts = [f"A single evocative cinematic frame that captures {subject}."]

    set_kind = d.get("set_kind")
    setting = {"INTERIOR": "an interior", "EXTERIOR": "an exterior"}.get(
        getattr(set_kind, "name", "")
    )
    if setting:
        parts.append(f"Set in {setting}.")

    # Styling tokens; skip the unmarked CONTEMPORARY era so it adds no noise.
    styling = [t.phrase for t in (d.get("medium_look"),) if t]
    era = d.get("era")
    if era is not None and getattr(era, "name", "") != "CONTEMPORARY":
        styling.append(era.phrase)
    if styling:
        parts.append("Rendered with " + " and ".join(styling) + ".")

    stance = d.get("concept_stance")
    if stance:
        parts.append("The design " + stance.phrase + ".")

    motifs = d.get("motifs") or []
    if motifs:
        parts.append("Recurring visual motifs: " + ", ".join(motifs) + ".")

    if plan.mood:
        parts.append("Mood: " + plan.mood.rstrip(".") + ".")

    # Counter gpt-image's literal reading of "poster" (a framed print in a room).
    parts.append(
        "Compose it as one cinematic production-design frame — a real scene in the "
        "world, not a printed poster, title text, or graphic layout."
    )
    return " ".join(parts)


def build_character_prompt(character: "Character", actor: "Actor") -> str:
    """Compose a :class:`~sequitur.cast.Character` and a candidate
    :class:`~sequitur.cast.Actor` into a still **character-reference** prompt (storyline 0054).

    The *audition* frame: the Actor's persona-authored ``look`` is the spine, the
    Character's design brief (age band, build, wardrobe) constrains it, and ``essence``
    colours the performance. Deliberately scene-agnostic and neutral — this renders the
    *person*, not an action beat, so it asks for a single consistent figure on a plain
    background: a clean reference the downstream renders (key art, shots) can lock the
    character's look to (Phase 3). Unlike :func:`build_image_prompt` it reads the cast
    entities, not a camera :class:`Shot`.
    """
    look = str(actor.look or "").strip()
    subject = (look or character.essence or character.role or character.name).rstrip(".")
    parts = [f"A cinematic character portrait of {subject}."]

    traits = [character.age_band.phrase]
    if character.build:
        traits.append(character.build.rstrip("."))
    parts.append("They are " + ", ".join(traits) + ".")

    if character.wardrobe:
        parts.append("Wardrobe: " + character.wardrobe.rstrip(".") + ".")
    # Essence adds an inner quality only when the look already carries the appearance.
    if character.essence and look:
        parts.append("Essence: " + character.essence.rstrip(".") + ".")

    parts.append(
        "A clean, evenly lit character reference: a single figure, head-and-shoulders "
        "to three-quarter length, with a consistent, clearly recognizable face and "
        "features, against a plain neutral background — a locked look to carry "
        "unchanged across later shots."
    )
    return " ".join(parts)


def build_key_art_prompt(
    concept: str,
    *,
    title: str,
    tagline: str | None = None,
    motifs: Sequence[str] = (),
    look: str | None = None,
    archetype: str | None = None,
    billing: bool = False,
    mood: str | None = None,
) -> str:
    """Compose a **theatrical one-sheet (key art)** prompt — the KeyArtist's arm.

    Unlike :func:`build_poster_prompt` (production art — a scene of the world), this
    asks for a *marketing poster* **with type**: a title treatment and an optional
    tagline, composed over the design concept. Empirically (the KeyArtist skill's
    grounding) ``gpt-image`` renders **headline** type legibly but garbles fine print,
    so the title/tagline are quoted for exact spelling and the ``billing`` block is
    **off by default**.

    This is the deterministic tier-A arm; the KeyArtist *skill* (tier B) supplies the
    judgement — which ``archetype`` to use, the ``title``/``tagline`` copy, and which
    ``motifs`` to foreground — all inherited from its parents (the Production Designer's
    concept and the story's marketing copy).
    """
    subject = concept.rstrip(".")
    parts = [
        "A theatrical movie poster (one-sheet), vertical portrait composition, "
        "professional high-end entertainment key art.",
        f"Central image: {subject}.",
    ]

    if archetype:
        parts.append(f"Composed as {archetype.rstrip('.')}.")
    if look:
        parts.append(f"Rendered with {look.rstrip('.')}.")
    if motifs:
        parts.append("Recurring visual motifs: " + ", ".join(motifs) + ".")

    parts.append(
        "Deliberately reserve clean negative space in the upper quarter and lower "
        "third for type."
    )

    parts.append(
        "Across the lower third, the FILM TITLE in a large, elegant, well-designed "
        f'treatment, perfectly spelled: "{title.strip()}".'
    )
    if tagline:
        parts.append(
            "In the upper quarter, a short tagline in small refined letter-spaced "
            f'capitals, perfectly spelled: "{tagline.strip()}".'
        )
    if billing:
        parts.append(
            "At the very bottom edge, a standard movie-poster billing block in tiny "
            "condensed credits text."
        )

    if mood:
        parts.append("Mood: " + mood.rstrip(".") + ".")

    parts.append(
        "All headline lettering must be crisp, correctly spelled, and legible; "
        "balanced graphic layout with clear focal hierarchy."
    )
    return " ".join(parts)
