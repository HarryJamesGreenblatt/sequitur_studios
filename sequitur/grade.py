"""The grammar of the grade — the color-finishing decision model.

Analogue of :mod:`sequitur.edit`: where the Editor's vocabulary composes an EDL,
the Colorist's vocabulary composes a **grade** — an ordered stack of colour-
correction operations applied to a rendered clip. Following the **Command** pattern
(a grade op is a *reified method call* — Nystrom, *Game Programming Patterns*), the
stack is:

* **ordered** — contrast before colour (Color Correction Handbook Ch. 3-4);
* **reified** — each op is a plain data object, so a whole grade serialises into a
  production plan (storyline 0005) exactly like the edit EDL (see :meth:`Grade.to_dict`);
* **executor-agnostic** — this module holds no ffmpeg/MoviePy dependency; turning a
  grade into pixels is the :class:`sequitur.grader.Grader` transform's job.

The vocabulary the Colorist reasons over (looks, tonal ranges, casts) is owned by
the :class:`~sequitur.crew.colorist.Colorist` role; this module is the aggregate
those choices compile into.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field

from .crew.colorist import TonalRange


@dataclass(frozen=True)
class GradeOp:
    """Base marker for a reified grade operation — a Command in the stack."""


@dataclass(frozen=True)
class Contrast(GradeOp):
    """Primary contrast: the luma lift / gamma / gain (Ch. 3).

    ``lift`` offsets the black point (-1..1), ``gamma`` redistributes the midtones
    (a power, 1.0 = neutral), ``gain`` scales the white point (1.0 = neutral).
    """

    lift: float = 0.0
    gamma: float = 1.0
    gain: float = 1.0


@dataclass(frozen=True)
class ColorBalance(GradeOp):
    """Primary colour balance for one tonal range (Ch. 4): an RGB push, -1..1."""

    range: TonalRange = TonalRange.MIDTONES
    r: float = 0.0
    g: float = 0.0
    b: float = 0.0


@dataclass(frozen=True)
class Saturation(GradeOp):
    """Master saturation (Ch. 4). 1.0 = unchanged, 0.0 = greyscale."""

    amount: float = 1.0


#: Reified op types, keyed by name — the basis of :meth:`Grade.from_dict`.
_OP_TYPES: dict[str, type[GradeOp]] = {
    "Contrast": Contrast,
    "ColorBalance": ColorBalance,
    "Saturation": Saturation,
}


@dataclass
class Grade:
    """A whole grade — an ordered, reified stack of ops bound to a rendered clip.

    ``source`` locates the artifact this grade transforms (the colour analogue of
    :attr:`sequitur.edit.Clip.source`); ``name`` is the look it came from.
    """

    ops: list[GradeOp] = field(default_factory=list)
    source: str | None = None
    name: str | None = None

    def add(self, op: GradeOp) -> "Grade":
        """Append an op to the stack. Chainable."""
        self.ops.append(op)
        return self

    @property
    def is_identity(self) -> bool:
        """True when the grade would leave the image unchanged."""
        return not self.ops

    def validate(self) -> list[str]:
        """Lint the stack; return human-readable issues.

        Errors: a non-positive gamma or negative gain/saturation. Warning: a colour
        op before the last contrast op — grade contrast first, colour second
        (Ch. 3-4).
        """
        issues: list[str] = []
        for op in self.ops:
            if isinstance(op, Contrast):
                if op.gamma <= 0:
                    issues.append("error: contrast gamma must be > 0")
                if op.gain < 0:
                    issues.append("error: contrast gain must be >= 0")
            elif isinstance(op, Saturation) and op.amount < 0:
                issues.append("error: saturation amount must be >= 0")

        first_color = next((i for i, o in enumerate(self.ops) if isinstance(o, ColorBalance)), None)
        last_contrast = max(
            (i for i, o in enumerate(self.ops) if isinstance(o, Contrast)), default=None
        )
        if first_color is not None and last_contrast is not None and first_color < last_contrast:
            issues.append(
                "warning: a colour op precedes a contrast op — grade contrast first, "
                "colour second (Ch. 3-4)"
            )
        return issues

    # -- serialization (Command pattern: the stack survives into a plan) -----

    def to_dict(self) -> dict:
        """A plain-data view of the grade — serialisable into a production plan."""

        def op_to_dict(op: GradeOp) -> dict:
            d: dict = {"op": type(op).__name__}
            for key, value in asdict(op).items():
                d[key] = value.name if isinstance(value, TonalRange) else value
            return d

        return {"name": self.name, "source": self.source, "ops": [op_to_dict(o) for o in self.ops]}

    @classmethod
    def from_dict(cls, data: dict) -> "Grade":
        """Rebuild a grade from its :meth:`to_dict` form."""
        ops: list[GradeOp] = []
        for od in data.get("ops", []):
            params = {k: v for k, v in od.items() if k != "op"}
            if "range" in params:
                params["range"] = TonalRange[params["range"]]
            ops.append(_OP_TYPES[od["op"]](**params))
        return cls(ops=ops, source=data.get("source"), name=data.get("name"))


# -- named-look registry ----------------------------------------------------
# Productions define their own looks when a built-in ``Look`` preset is not
# enough. A look is just a ``Grade``, so a production-defined look is a named
# ``Grade`` template that serialises into a production plan (storyline 0005) for
# free via ``to_dict`` — the open-tag complement to the closed ``Look`` enum.

_LOOKS: dict[str, Grade] = {}


def register_look(name: str, grade: Grade) -> None:
    """Register a production-defined named look — a reusable :class:`Grade` template.

    Reached by name through :meth:`sequitur.crew.colorist.Colorist.grade`; overwrites
    any look already registered under ``name``.
    """
    _LOOKS[name] = grade


def named_look(name: str, *, source: str | None = None) -> Grade:
    """Resolve a registered look to a *fresh* :class:`Grade` bound to ``source``.

    Returns a copy so the stored template is never mutated by a caller binding a
    source or extending the stack.
    """
    try:
        template = _LOOKS[name]
    except KeyError:
        raise LookupError(f"No look registered under {name!r}.") from None
    return Grade(ops=list(template.ops), source=source, name=template.name or name)


def registered_looks() -> tuple[str, ...]:
    """The names of all production-defined looks."""
    return tuple(_LOOKS)
