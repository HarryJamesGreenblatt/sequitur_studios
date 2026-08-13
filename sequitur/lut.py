"""LUT authoring — compile a reified :class:`~sequitur.grade.Grade` into a 3D LUT.

The Grader's execution moved from arbitrary ffmpeg ``eq``/``colorbalance`` filters
(storyline 0022) to the industry-standard path (storyline 0024): bake a grade's
**primaries** into a 3D LUT and let ffmpeg apply it via ``lut3d``. This module is the
**authoring** stage — a grade in, a spec-correct Iridas ``.cube`` out — built on
**colour-science** so the two standards-critical, easy-to-cook parts (the ASC CDL
math and the ``.cube`` file format) are handled by a battle-tested library rather
than hand-rolled.

*Primaries only.* Contrast (ASC CDL slope/offset/power), per-zone colour balance,
and saturation bake cleanly into a global 3D LUT. Secondaries (HSL qualification,
shape windows) are spatially/chroma-gated and cannot live in a global LUT — they
remain a separate masked-pass concern (deferred).

The bake is a **pure function** (a grade → a ``colour.LUT3D``), so the colour math is
unit-testable without an ffmpeg binary; only :mod:`sequitur.grader` shells out.
"""

from __future__ import annotations

import warnings
from pathlib import Path

import numpy as np

with warnings.catch_warnings():  # silence colour's optional-scipy/matplotlib notices
    warnings.simplefilter("ignore")
    from colour.io import LUT3D, write_LUT

from .crew.colorist import TonalRange
from .grade import ColorBalance, Contrast, Grade, Saturation

#: Rec. 709 luma weights (Color Correction Handbook Ch. 3: ~21% R / 72% G / 7% B).
_LUMA = np.array([0.2126, 0.7152, 0.0722])

#: Default lattice resolution — 33³ is the broadcast / DaVinci default.
DEFAULT_SIZE = 33


def bake(grade: Grade, *, size: int = DEFAULT_SIZE) -> "LUT3D":
    """Bake a grade's primary ops into a :class:`colour.LUT3D` (a pure function).

    Applies each op to the identity lattice in stack order — so contrast precedes
    colour precedes saturation (the grade validated that ordering). Returns the LUT
    without writing a file, so the maths is testable without ffmpeg.
    """
    table = LUT3D.linear_table(size)  # (size, size, size, 3), values 0..1
    rgb = table.reshape(-1, 3).astype(float)
    for op in grade.ops:
        rgb = _apply(op, rgb)
    rgb = np.clip(rgb, 0.0, 1.0)
    return LUT3D(rgb.reshape(size, size, size, 3), name=grade.name or "grade", size=size)


def write_cube(grade: Grade, path: str | Path, *, size: int = DEFAULT_SIZE) -> Path:
    """Bake ``grade`` and write it as an Iridas ``.cube`` at ``path``; returns it."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        write_LUT(bake(grade, size=size), str(path))
    return path


# -- per-op maths (baked into every lattice node) ---------------------------


def _apply(op, rgb: np.ndarray) -> np.ndarray:
    """Apply one grade op to an (N, 3) array of RGB samples."""
    if isinstance(op, Contrast):
        # ASC CDL SOP: out = (in · slope + offset) ^ power, per channel
        # (slope=gain, offset=lift, power=gamma). Clip before the power so a
        # negative base never meets a fractional exponent (→ nan).
        out = np.clip(rgb * op.gain + op.lift, 0.0, 1.0)
        return out**op.gamma
    if isinstance(op, ColorBalance):
        # Per-zone RGB offset, weighted by a smooth luma zone-membership.
        weight = _zone_weight(op.range, rgb @ _LUMA)[:, None]
        return rgb + weight * np.array([op.r, op.g, op.b])
    if isinstance(op, Saturation):
        # out = luma + amount · (rgb − luma), Rec. 709 luma.
        lum = (rgb @ _LUMA)[:, None]
        return lum + op.amount * (rgb - lum)
    return rgb


def _zone_weight(zone: TonalRange, lum: np.ndarray) -> np.ndarray:
    """Smooth, overlapping shadow / mid / highlight weights that sum to 1 over luma."""
    shadows = np.clip(1.0 - 2.0 * lum, 0.0, 1.0)
    highlights = np.clip(2.0 * lum - 1.0, 0.0, 1.0)
    if zone is TonalRange.SHADOWS:
        return shadows
    if zone is TonalRange.HIGHLIGHTS:
        return highlights
    return 1.0 - shadows - highlights  # midtones: a triangular peak at mid-grey
