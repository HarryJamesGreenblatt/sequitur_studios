# 0024 — The Production Board (Azure DevOps as the PM-board backing)

> Date: 2026-08-12 · Focus: **infrastructure + design** — realized the `0008` decision
> that *the Production **is** the PM board* by standing up the actual board on **Azure
> DevOps** and modelling the narrative hierarchy as a custom work-item process. This was
> the platform choice `0005` left deferred. **No `sequitur/` code changed** — groundwork
> for the coming `ProductionProvider` seam.

---

## What happened

- **Picked the PM-board backing — Azure DevOps over Microsoft Planner.** `0008` said the
  Production *is* the PM board (Planner / ADO / GH Projects), and `0005` deferred the
  platform. Both candidates were auth-proven from the local `az login` (a
  `DefaultAzureCredential` Graph token reads Planner; the same identity mints an ADO
  token), so the decision came down to the data model: **Planner is essentially two
  levels** (plan → bucket → task) while the EDL is **four** (Act → Scene → Beat → Shot).
  ADO's work-item hierarchy carries all four natively — the deciding factor.

- **Modelled the board as a custom inherited process.** Rather than mentally map the EDL
  onto stock type names, built a custom process (**parent = Basic**, chosen for its
  leanness over Agile's Bug/Test/Feature clutter) with four **domain-named work-item
  types — Act / Scene / Beat / Shot** — each wired to a backlog level. Basic ships three
  levels (Epic/Issue/Task); a **new top portfolio level** was added for **Act** above
  them. The inherited Basic types are **disabled** for a focused **+ New** menu. States
  are **To do / Doing / Done**.

- **Departments = Area Paths.** The seven crew departments (Direction, Camera, Lighting,
  Grip, Editorial, Color, Sound) are **Area Paths** — a categorization axis *orthogonal*
  to workflow state. This is the ADO-native form of the "bucket = layer/department"
  intuition that first drew us to Planner, and it realizes the `0008` "crew picks up its
  own bucket" idea: e.g. the `Colorist` can query all shots in the `Color` area.

- **A project = one Production instance (`0005`).** Created a project on the custom
  process; its work items are one production's Act→Scene→Beat→Shot tree.

- **Tooling.** Work-item CRUD runs through the official **Azure DevOps MCP** (`wit_*`
  tools) — the same MCP-client pattern as toaster-strudel (`0009`). Process customization
  is a mix of REST and portal: creating the custom types and disabling inherited ones is
  scriptable, but the **backlog-level ("behaviors") wiring is done in the portal** because
  that REST surface is too thin (confirmed against first-party docs, after some guessing).

## Decisions

1. **Production board = Azure DevOps, not Planner or a local folder.** ADO for the
   four-level hierarchy and typed fields; Planner's flat plan→bucket→task can't hold
   Act→Scene→Beat→Shot without collapsing a level. The local folder stays useful only as
   a test double for the provider seam.

2. **Basic base + fresh custom types, not renamed system types.** First-party docs
   settled two things that were being guessed at: (a) you **can't rename system work-item
   types** — you create fresh custom ones; and (b) **parent/child hierarchy is set by
   backlog-level assignment, not by `inheritsFrom`** (each system type can be inherited
   only once, so inheriting is a dead end for domain names). Custom backlog levels can
   only be added at the **top**, which is exactly where Act belongs.

3. **Four orthogonal axes, where Planner smushes two.** Narrative → the WIT hierarchy;
   department/layer → **Area Path**; workflow → **State**; phase → *(deferred: iteration
   or a field)*. Keeping department off the status axis is precisely what makes
   department-scoped crew queries possible.

4. **MCP is the Producer's data-plane surface; the `ProductionProvider` reads/writes the
   board via SDK.** The MCP drives the board conversationally (the human Producer's
   surface); the *library's* own `read_brief()` / `write_sequence()` will call the
   ADO/Graph API directly via `DefaultAzureCredential` — the same seam idea as the
   `Renderer` protocol (`0021`), and backend-swappable (Planner or a local folder could
   sit behind the same interface).

5. **Model lean.** The board holds *Producer/brief-level* data (mood, look, department,
   status, the shot list); the crew engine still computes the full grammar. Only two
   fields (`Mood`, `Look` on Shot) are planned — not a grammar-enum dump.

## Resulting state

- The studio's Azure DevOps organization now hosts a custom **Basic-derived process**
  (Act → Scene → Beat → Shot as a 4-level work-item hierarchy, inherited types disabled,
  states To do / Doing / Done) and **one project** (a Production instance) on it, with the
  seven **department Area Paths**. Validated end-to-end through the ADO MCP. Concrete
  identifiers (org / project / process names + IDs, tenant) live only in gitignored local
  notes and `.env`, per the no-infra-names-in-shipped-docs rule.
- **No `sequitur/` code changed** — this session was infrastructure and design groundwork.

## Open threads

- **Fields `Mood` + `Look` on Shot** — the last modelling bit; the ADO picklist/field
  REST flow (research-first, like the work-item types).
- **Build the `ProductionProvider` seam (`0005`/`0008`)** — `read_brief()` (board tree →
  `Brief`; coverage `shots` from the Shot work items; department from Area Path) and
  `write_sequence()` (the graded `Sequence` → work-item state/fields), mirroring the
  `Renderer` protocol. Scaffold an example Act→Scene→Beat→Shot tree via the MCP as its
  first read target.
- **Phase axis** — represent plan / shoot / assemble as an iteration or a Shot field.
- **App-only auth** — a registered least-privilege app for unattended/CI use (interactive
  `az login` / `DefaultAzureCredential` covers local today).
- Cosmetic: set Shot as the iteration-backlog default; optionally disable the Test types.
