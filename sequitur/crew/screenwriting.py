"""The story department — the **Screenwriter** (plan phase).

Owns the studio's story vocabulary: Eric R. Williams' *Screenwriter's Taxonomy* as a
**layered descriptor vector** (storyline 0016). Where the DP owns a few closed camera
enums, the Screenwriter owns the whole seven-layer classification:

* :class:`MovieType` (Comedy/Drama) and the closed eleven-value :class:`Supergenre`
  (Ch. 2) — the umbrella that *defines* Story / Character / Atmosphere;
* :class:`Macrogenre` (a large, curated, **multiple-allowed** modifier enum) plus an
  open, macro-scoped **microgenre** tag (plain ``str`` — 200+ and meant to grow, Ch. 3);
* :class:`Voice` — a *struct* of six orthogonal axes (Ch. 5), the seam where the story
  layer reaches into the render grammar (medium → backend, dialogue mode → sound);
* :class:`Pathway` — the closed twenty-value trajectory the audience travels (Ch. 6);
* point of view as **three small enums** — :class:`Scope` × :class:`Focus` ×
  :class:`Stance` (Ch. 7) — the direct upstream of camera coverage.

This is **vocabulary + a heuristic default**, the plan-phase analogue of the shoot
crew's ``crew/camera.py`` (storyline 0012): the Screenwriter's :class:`Contribution`
is a *story descriptor*, not a :class:`~sequitur.shot.Shot`. A plan-phase reconcile
(a Director/Engine that turns the descriptor into downstream briefs) is a later pass —
this module gives the seat its owned language first.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING, Any

from .role import Department, Phase, Role

if TYPE_CHECKING:
    from ..plan import Plan
    from .role import Brief


class MovieType(Enum):
    """The taxonomy's most basic split — funny or serious (Ch. 2)."""

    COMEDY = ("a comedy", "fundamentally funny — twelve brands, farce to satire")
    DRAMA = ("a drama", "fundamentally serious — ten brands, tragedy to docudrama")

    def __init__(self, phrase: str, intent: str) -> None:
        self.phrase = phrase
        self.intent = intent


class Supergenre(Enum):
    """The eleven umbrellas that define Story / Character / Atmosphere (Ch. 2).

    A closed enum — the story-layer analogue of ``ShotSize``. Selecting one is a
    *bundle*, not a label: its location/costume/visceral expectations seed the
    Production Designer and DP, its theme/rhythm the Editor's pacing.
    """

    ACTION = ("action", "resourceful hero vs. single-minded villain; Good vs. Evil")
    CRIME = ("crime", "criminal vs. lawman; truth, justice, freedom")
    FANTASY = ("fantasy", "wonderment; personal stakes; the Hero's Journey")
    HORROR = ("horror", "sin vs. purity; a group whittled by an unseen aggressor")
    LIFE = ("day-in-the-life", "we all share the same struggles; one lead or an ensemble")
    ROMANCE = ("romance", "love in its many axioms; two equal protagonists")
    SCIENCE_FICTION = ("science fiction", "the unknown; social critique via metaphor")
    SPORTS = ("sports", "our team vs. theirs; the underdog and the Big Game")
    THRILLER = ("thriller", "unwitting hero vs. epic villain; hope and fear")
    WAR = ("war", "the will to survive; sacrifice")
    WESTERN = ("western", "law vs. chaos; taming the wild")

    def __init__(self, phrase: str, intent: str) -> None:
        self.phrase = phrase
        self.intent = intent


class Macrogenre(Enum):
    """A large, curated modifier enum — *refines* a supergenre (Ch. 3).

    Interchangeable and **multiple-allowed** (a Contribution carries a list): Crime +
    Addiction + Gangster = *Scarface*. The list is curated, not exhaustive — meant to
    grow. Its value is the display phrase.
    """

    ADDICTION = "addiction"
    ADVENTURE = "adventure"
    ALIEN_INVASION = "alien invasion"
    ARTIFICIAL_INTELLIGENCE = "artificial intelligence"
    APOCALYPTIC = "apocalyptic"
    BIOGRAPHY = "biography"
    BROMANCE_WOMANCE = "bro-/womance"
    DEMONIC = "demonic"
    DISASTER = "disaster"
    DISEASE_DISABILITY = "disease/disability"
    EPIC_SAGA = "epic/saga"
    EROTICA = "erotica"
    ESCAPE = "escape"
    FAMILY = "family"
    GANGS = "gangs"
    GANGSTER = "gangster"
    GHOST_SPIRITS = "ghost/spirits"
    HEIST_CAPER = "heist/caper"
    HISTORICAL = "historical"
    HOLIDAY = "holiday"
    IDENTITY = "identity"
    KILLING = "killing"
    LAW_ENFORCEMENT = "law enforcement"
    LEGAL = "legal"
    LOVE = "love"
    MAGICAL = "magical"
    MARTIAL_ARTS = "martial arts"
    MEDICAL = "medical"
    MILITARY = "military"
    MISSION = "mission"
    MONSTER = "monster"
    MYSTERY_DETECTIVE = "mystery/detective"
    POLITICAL = "political"
    PROCEDURAL = "procedural"
    PROTECTION = "protection"
    PSYCHOLOGICAL = "psychological"
    RELIGIOUS = "religious"
    REVENGE_JUSTICE = "revenge/justice"
    ROMANTIC_COMEDY = "romantic comedy"
    SCIENCE_FANTASY = "science fantasy"
    SCHOOL = "school"
    SHOWBIZ = "showbiz"
    SLASHER = "slasher"
    SPY_ESPIONAGE = "spy/espionage"
    SUPERHERO = "superhero"
    SUPERPOWERS = "superpowers"
    SURVIVAL = "survival"
    TERROR = "terror"
    TIME_TRAVEL = "time travel"
    WORKPLACE = "workplace"

    @property
    def phrase(self) -> str:
        return self.value


# -- Voice: a struct of six orthogonal axes (Ch. 5) -----------------------------


class Linearity(Enum):
    """How time is ordered — the traditional default is ``LINEAR``."""

    LINEAR = "a linear narrative"
    FLASHBACK = "flashback structure"
    INTERCUT_TIMELINES = "two time periods intercut"
    PARALLEL_REALITIES = "parallel realities"
    LOOP = "a repetition / time loop"
    TIME_TRAVEL = "time-travel-scrambled order"
    REVERSE_CHRONOLOGY = "reverse chronology"

    @property
    def phrase(self) -> str:
        return self.value


class FilmmakingStyle(Enum):
    """The technical register — the traditional default is ``MODERN``."""

    MODERN = "modern technique (colour, coverage, complex sound)"
    MONOCHROME = "black-and-white (or selective colour)"
    MINIMALIST = "minimalist / creative silence"
    LONG_TAKE = "long takes / slow rhythm"

    @property
    def phrase(self) -> str:
        return self.value


class Audience(Enum):
    """The content ceiling across language/violence/humour/sexuality/gore."""

    KIDS = "a kids' audience"
    BROAD = "a broad audience"
    MATURE = "a mature / adult audience"

    @property
    def phrase(self) -> str:
        return self.value


class Performer(Enum):
    """The performing medium — a *form*, not a genre; default ``LIVE_ACTION``."""

    LIVE_ACTION = "live-action human performers"
    ANIMATION = "animation"
    PUPPETS = "puppets"
    STOP_MOTION = "stop-motion"

    @property
    def phrase(self) -> str:
        return self.value


class DialogueMode(Enum):
    """How interiority reaches the audience — default ``SPOKEN``."""

    SPOKEN = "spoken dialogue"
    MUSICAL = "musical numbers"
    SILENT = "silence / no dialogue"
    VOICEOVER = "internal monologue / voice-over"

    @property
    def phrase(self) -> str:
        return self.value


class FourthWall(Enum):
    """The fourth wall — default ``INTACT`` (oblivious participants)."""

    INTACT = "an intact fourth wall"
    BROKEN = "direct address (broken fourth wall)"
    MOCKUMENTARY = "a mockumentary frame"

    @property
    def phrase(self) -> str:
        return self.value


@dataclass
class Voice:
    """*How* the story is told — a bundle of six orthogonal axes (Ch. 5).

    Unlike the single-choice :class:`Supergenre`, Voice is a struct (like a
    :class:`~sequitur.shot.Shot` is a bundle of grammar fields). Its defaults are the
    book's **traditional voice**: linear, modern, broad, live-action, spoken, oblivious.
    Its axes are the seam into the render grammar — ``performer`` selects the backend,
    ``dialogue_mode`` routes the sound layer, ``linearity`` is a directive the Editor
    executes.
    """

    linearity: Linearity = Linearity.LINEAR
    style: FilmmakingStyle = FilmmakingStyle.MODERN
    audience: Audience = Audience.BROAD
    performer: Performer = Performer.LIVE_ACTION
    dialogue_mode: DialogueMode = DialogueMode.SPOKEN
    fourth_wall: FourthWall = FourthWall.INTACT


# -- Pathway: the audience's trajectory (Ch. 6) ---------------------------------


class Pathway(Enum):
    """The trajectory the audience travels — a closed twenty-value enum (Ch. 6).

    ``TRADITIONAL`` is the Hero's-Journey baseline; every other pathway breaks at
    least one of its five elements (single-protagonist · audience-learns-with-hero ·
    returns-home · hero-battles-antagonist · hero-rewarded). The ``breaks`` note names
    the divergence — the metadata the shoot/post crews read (multi-protagonist →
    coverage split; audience-ahead → dramatic irony for the Editor).
    """

    TRADITIONAL = ("the traditional Hero's Journey", "breaks none — the baseline")
    NOIR = ("a noir descent", "breaks #4/#5 — the real foe is a larger force; the hero loses even winning")
    TALE_OF_MADNESS = ("a tale of madness", "breaks #4/#5 — the antagonist is the protagonist's own mind")
    RAGS_TO_RICHES_TO_RAGS = ("rags to riches to rags", "breaks #5 — the rise is undone; survival is the only win")
    MELODRAMA = ("a melodrama", "breaks #1/#5 — the hero rarely changes; catharsis lands in the audience")
    CHASE_HUNT = ("a chase / hunt", "breaks #3 — the hero is prey and never returns home")
    ROAD_MOVIE = ("a road movie", "breaks #3 — perpetually in transit, no home to return to")
    BUDDY_MOVIE = ("a buddy movie", "breaks #1 — two leads at odds share the story")
    SCREWBALL_COMEDY = ("a screwball comedy", "breaks #1 — a sparring pair split the protagonism")
    REUNITE_THE_GANG = ("reunite the gang", "breaks #1 — the story fans across several leads")
    UNLIKELY_ENSEMBLE = ("an unlikely ensemble", "breaks #1 — a mismatched group carries it together")
    REUNION = ("a reunion", "breaks #1/#2 — the audience joins relationships already in progress")
    GANG_FALLS_APART = ("the gang falls apart", "breaks #1/#2 — track each lead's arc and the order of each demise")
    COMING_OF_AGE = ("a coming of age", "breaks #2 — the audience remembers rather than learns")
    LOST_INNOCENCE = ("lost innocence", "breaks #2 — we watch an awakening we already understand")
    FISH_OUT_OF_WATER = ("a fish out of water", "breaks #4 — the antagonist is a displacing environment")
    HUMAN_VS_NATURE = ("human vs. nature", "breaks #4 — the antagonist is the natural world / disaster")
    HUMAN_VS_SELF = ("human vs. self", "breaks #4 — the antagonist is the protagonist within")
    HUMAN_VS_SOCIETY = ("human vs. society", "breaks #4 — the antagonist is the social order")
    HUMAN_VS_TECHNOLOGY = ("human vs. technology", "breaks #4 — the antagonist is a machine / system")

    def __init__(self, phrase: str, breaks: str) -> None:
        self.phrase = phrase
        self.breaks = breaks


# -- Point of view: three small enums whose product names a POV (Ch. 7) ---------


class Scope(Enum):
    """How much the audience is allowed to know."""

    LIMITED = "limited to what the protagonist knows"
    OMNISCIENT = "omniscient — reveal any character at any time"

    @property
    def phrase(self) -> str:
        return self.value


class Focus(Enum):
    """Through whom the story is told."""

    PRIMARY = "told through the protagonist"
    SECONDARY = "told through another character"

    @property
    def phrase(self) -> str:
        return self.value


class Stance(Enum):
    """Whether what we are shown is reliable."""

    OBJECTIVE = "an objective, reliable account"
    SUBJECTIVE = "a subjective, questionable account"

    @property
    def phrase(self) -> str:
        return self.value


class Screenwriter(Role):
    """The story department head — owns the taxonomy vocabulary (plan phase).

    Its :class:`~sequitur.crew.role.Contribution` is a *story descriptor* (the layered
    vector), not a :class:`~sequitur.shot.Shot`: the plan-phase seat that classifies the
    story the shoot and post crews then realise. POV is the sharpest downstream link —
    ``scope``/``focus`` constrain the DP's coverage and the Editor's cross-cutting.
    """

    title = "Screenwriter"
    department = Department.STORY
    phase = Phase.PLAN
    vocabulary = (
        MovieType,
        Supergenre,
        Macrogenre,
        Linearity,
        FilmmakingStyle,
        Audience,
        Performer,
        DialogueMode,
        FourthWall,
        Pathway,
        Scope,
        Focus,
        Stance,
    )

    def heuristic(self, brief: Brief) -> dict[str, Any]:
        # The neutral descriptor: a linear, broad, objective slice-of-life — the
        # cheapest-to-render umbrella (Ch. 2 studio note); hints override any field.
        h = brief.hints
        return {
            "movie_type": h.get("movie_type", MovieType.DRAMA),
            "supergenre": h.get("supergenre", Supergenre.LIFE),
            "macrogenres": list(h.get("macrogenres", [])),
            "microgenres": list(h.get("microgenres", [])),
            "voice": h.get("voice", Voice()),
            "pathway": h.get("pathway", Pathway.TRADITIONAL),
            "scope": h.get("scope", Scope.LIMITED),
            "focus": h.get("focus", Focus.PRIMARY),
            "stance": h.get("stance", Stance.OBJECTIVE),
        }

    def treatment(self, plan: Plan) -> str:
        """Compose a human-readable **treatment** from a plan's story descriptor (tier A).

        The deterministic template: a coherent prose derivation of the taxonomy layers
        (the dailies-model plan deliverable, storyline 0036/0047). The Screenwriter
        *persona* (B) narrates the full treatment from its Glebas / Directing grounding —
        the payload the descriptor can classify but not narrate; this A version is the
        offline, testable baseline the persona replaces.
        """
        s = plan.story
        scene = plan.scene.rstrip(".")
        opening = (scene[:1].upper() + scene[1:]) if scene else "This production"
        phr = lambda x: getattr(x, "phrase", None)  # noqa: E731

        lines = [f"# Treatment — {scene}", ""]

        # Logline: genre + modifiers, from labels only (never the enums' internal
        # intent/breaks glosses, which are design metadata, not prose).
        mt, sg = s.get("movie_type"), s.get("supergenre")
        logline = opening
        if sg is not None:
            mt_word = (phr(mt) or "").split()[-1]  # "a drama" -> "drama"
            logline += f" is a {phr(sg)}{' ' + mt_word if mt_word else ''}"
        macros = s.get("macrogenres") or []
        if macros:
            logline += ", turning on " + ", ".join(phr(m) for m in macros)
            micro = s.get("microgenres") or []
            if micro:
                logline += " (" + ", ".join(micro) + ")"
        lines.append(logline.rstrip() + ".")

        pw = s.get("pathway")
        if pw is not None:
            lines.append("The audience follows " + phr(pw) + ".")

        pov = [phr(x) for x in (s.get("scope"), s.get("focus"), s.get("stance")) if x]
        if pov:
            lines.append("Point of view: " + "; ".join(pov) + ".")

        voice = s.get("voice")
        if voice is not None:
            vbits = [phr(voice.linearity), phr(voice.style), phr(voice.dialogue_mode)]
            aud = phr(voice.audience)
            lines.append("Voice: " + ", ".join(b for b in vbits if b) + (f" — for {aud}." if aud else "."))

        if plan.mood:
            lines += ["", f"*Mood:* {plan.mood.rstrip('.')}."]

        lines += [
            "",
            "*(Structural outline from the story descriptor — the Screenwriter persona "
            "narrates the full treatment from its Glebas / Directing grounding.)*",
        ]
        return "\n".join(lines)
