"""The Director — the reconciler that assembles the crew's contributions.

The Director is itself a :class:`~sequitur.crew.role.Role`, but its job is not to
own a vocabulary — it is to reconcile the rest of the crew into a single decision
(storyline 0008: "agency lives in a component, never the container"). In the shoot
phase that decision is a :class:`~sequitur.shot.Shot`: each department fills its
*owned* fields and the Director merges them. Because the departments own disjoint
slices of the shot, the merge is conflict-free.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from ..render import Medium, RenderResult, renderer_for
from ..shot import Shot
from .role import Department, Phase, Role

if TYPE_CHECKING:
    from ..edit import Sequence
    from ..gate import Deliverable, Gate
    from ..output import OutputStore
    from ..plan import Plan
    from .role import Brief, Contribution


class Director(Role):
    """Reconciles the crew's contributions into a single decision (a Shot)."""

    title = "Director"
    department = Department.DIRECTION

    def reconcile(self, brief: Brief, contributions: list[Contribution]) -> Shot:
        """Merge the crew's owned fields into a complete :class:`Shot`."""
        fields: dict = {}
        for contribution in contributions:
            for key, value in contribution.fields.items():
                if value is not None:
                    fields[key] = value
        return Shot(
            scene=brief.scene,
            mood=brief.mood,
            audio=brief.audio,
            aspect_ratio=brief.aspect_ratio,
            **fields,
        )

    def plan(self, brief: Brief, contributions: list[Contribution]) -> Plan:
        """Reconcile the plan crew into a :class:`~sequitur.plan.Plan`.

        The Screenwriter contributes the story descriptor, the Production Designer the
        design descriptor; the Director groups each seat's owned slice into the plan's
        story/design halves. Like the shoot and assemble reconciles the fields are
        disjoint, so grouping is loss-free. Unlike them the result is a *Plan*, not a
        renderable :class:`Shot` — the intent the later phases realise, and the source of
        the dailies-model treatment (story) and poster (design).
        """
        from ..plan import Plan
        from .production_design import ProductionDesigner

        story: dict = {}
        design: dict = {}
        for contribution in contributions:
            target = design if contribution.role == ProductionDesigner.title else story
            for key, value in contribution.fields.items():
                if value is not None:
                    target[key] = value
        return Plan(
            scene=brief.scene,
            mood=brief.mood,
            aspect_ratio=brief.aspect_ratio,
            story=story,
            design=design,
        )

    def deliver_plan(
        self,
        plan: Plan,
        *,
        gate: Gate,
        out_path: str | Path | None = None,
        treatment: str | None = None,
    ) -> list[Deliverable]:
        """Produce the plan phase's two dailies deliverables and submit them to a gate.

        The storyline-0036 first slice: a **treatment** (from ``plan.story``) and a
        **poster** (from ``plan.design``, composed by
        :func:`~sequitur.prompt.build_poster_prompt` and rendered through the still
        backend). Each is filed durably via the :class:`~sequitur.gate.Gate` and returned
        as a PENDING :class:`~sequitur.gate.Deliverable` for the Producer's review.

        Two tiers feed this. By default the deterministic **A** composers run: the
        Screenwriter's :meth:`~sequitur.crew.screenwriting.Screenwriter.treatment`
        skeleton and a poster from ``plan.design`` (whose ``visual_concept`` is blank in
        the heuristic, so the frame falls back to the scene). Pass a persona-authored
        ``treatment`` (the Screenwriter **B** agent's narrated version) and seat a real
        ``visual_concept`` on the plan's design (the Production Designer **B** agent) to
        get the meaningful daily — the A path is only the offline baseline.
        """
        from ..prompt import build_poster_prompt
        from .screenwriting import Screenwriter

        text = treatment if treatment is not None else Screenwriter().treatment(plan)
        story_deliverable = gate.submit(
            text.encode("utf-8"), phase=Phase.PLAN, name="treatment.md"
        )

        poster = renderer_for(Medium.STILL).render(build_poster_prompt(plan), out_path=out_path)
        poster_deliverable = gate.submit(poster.ref, phase=Phase.PLAN, name="poster.png")

        return [story_deliverable, poster_deliverable]

    def execute(
        self,
        shot: Shot,
        *,
        medium: Medium = Medium.VIDEO,
        out_path: str | Path | None = None,
        store: OutputStore | None = None,
        production: str | None = None,
        phase: str = "shoot",
        name: str | None = None,
    ) -> RenderResult:
        """Close decision -> pixels (-> durable): render a greenlit :class:`Shot`.

        Reconciling chooses the shot; this hook *executes* it. It resolves the
        producer for ``medium`` from the renderer registry (storyline 0021) and hands
        it the Shot, which the backend composes through
        :func:`~sequitur.prompt.build_prompt`. Video (Gemini Omni) and still
        (``gpt-image``) are the media that render a Shot; the default is video, the
        studio's headline medium. The Director stays backend-agnostic — it holds a
        renderer *by medium*, never a concrete class.

        A renderer writes to a *scratch* path. Pass a ``store`` (with the owning
        ``production``) to also file that artifact durably under ``phase`` and return
        a :class:`~sequitur.render.RenderResult` whose ``ref`` is the durable location
        (storyline 0038) — the dailies model's render -> persist step, ready for a gate.
        """
        result = renderer_for(medium).render(shot, out_path=out_path)
        if store is None:
            return result
        if not production:
            raise ValueError("Storing a render requires the owning production.")
        ref = store.put(result.ref, production=production, layer=phase, name=name)
        return RenderResult(raw=result.raw, ref=ref)

    def assemble(self, brief: Brief, contributions: list[Contribution]) -> Sequence:
        """Reconcile the assemble crew into a graded edit :class:`~sequitur.edit.Sequence`.

        The Editor contributes the cut structure (``cut``), the Colorist a base
        ``grade``; the Director lays the coverage into one scene, attaching a copy of
        the base grade to each clip (the anchor look — per-shot matching, Ch. 9, is a
        later refinement).
        """
        from ..edit import Act, Beat, Clip, Edit, Scene, Sequence
        from ..grade import Grade
        from .editorial import EditReason, Transition

        fields: dict = {}
        for contribution in contributions:
            for key, value in contribution.fields.items():
                if value is not None:
                    fields[key] = value
        cut = fields.get("cut", [])
        base = fields.get("grade")

        scene = Scene()
        for i, shot in enumerate(brief.shots):
            transition, reason = (
                cut[i] if i < len(cut) else (Transition.CUT, EditReason.INFORMATION)
            )
            grade = Grade(ops=list(base.ops), name=base.name) if base is not None else None
            scene.beats.append(
                Beat(Clip(shot, grade=grade), Edit(transition=transition, reason=reason))
            )
        return Sequence(acts=[Act(scenes=[scene])], aspect_ratio=brief.aspect_ratio)
