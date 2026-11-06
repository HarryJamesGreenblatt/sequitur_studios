# 0064 - Session handoff and canonical checkout

> Date: 2026-11-05. Focus: capture the complete Sequitur alignment session for the
> next agent, then establish a clean, properly named engine checkout after merge.

This handoff is committed as Task #40 **before** the merge and clone. The cutover
steps below are the approved plan, not a claim that those later operations already
happened. Retrieve the engine PBI/PR and governing workspace's private cutover
record for their final status, merge hash and canonical path.

## Why this session happened

SpeakerSplitter had developed a cohesive ADO-as-RAG engineering loop: read the
board/wiki, implement criterion-sized Tasks, commit each Task, present the linked
PR, and update the board continuously. Studios had a richer film-production model
but mixed shared engine behavior with workstation-local production inputs/state.
The user wanted the same organizational discipline, not conversion of film craft
into Scrum or a separate engine fork for every production.

The governing workspace is **Sequitur**, with separate organization scopes.
The first additive shell fixed instruction/MCP routing but still presented the
engine as an apparent parent production. The subsequent correction established
real peer production homes and explicit runtime bindings; see 0063.

## The agreed ownership model

| Scope | Owns | Publishing/tracking |
|---|---|---|
| Governing Sequitur workspace | Shared routing, organization profiles, local registry and startup | Local governance; do not infer an organization from a process name |
| Scrum organization | Independent engineering projects, initially SpeakerSplitter | Each project has its own ADO Git home and GitHub mirror |
| Shared Studios engine | Crew behavior, agents, skills, grounding, render/provider/store code and engine history | One engine Git history: ADO primary/PR home, existing GitHub mirror |
| Studios production | Its brief, decisions, inputs, casting state, artifact namespace and phase approvals | ADO-only production management with a private nested local home; no engine fork or GitHub mirror |

Processes are **project-scoped**. The engine's engineering project uses Scrum.
The three existing production projects retain their custom Basic-derived
film-production process. The engine's Scrum process does not move it to the
sibling Scrum organization.

The production model remains Cut > Act > Scene > Beat > Shot, with separate
Deliverable, Cast and Marketing Asset review types. Departments/teams, phases and
workflow state are independent axes. The Producer remains the human approval
authority; the Director reconciles and the craft seats own their judgments.

## What was implemented

1. **Explicit instruction layers.** Governing, organization and project guidance
   are separate and conditionally scoped. Both harnesses get an explicit bootstrap;
   arbitrary parent inheritance and universal child-file precedence are not assumed.
2. **Organization-scoped MCP.** The stock server supplies work items, wiki, PRs
   and repository reads. Enabling domains had provided earlier flexibility, but
   stock version 2.11.0 did not expose project/repository creation. The versioned
   companion in `tools\ado-admin-mcp` supplies typed administration with no arbitrary
   request, deletion or process-conversion operation. Its skill documents the flow.
3. **Engine delivery.** A private ADO engineering project/repository was provisioned
   through MCP. `ado` is primary; `origin` keeps its existing GitHub fetch URL and
   both GitHub/ADO push URLs. The Git helper uses temporary, organization-scoped
   Entra authorization without storing tokens.
4. **Peer production homes.** Each confirmed production has `production.json`,
   `.github`, `context`, `inputs`, `state` and `.local\scratch`. These homes are
   outside the public engine repository.
5. **Explicit execution binding.** `ProductionWorkspace` and
   `scripts\production_workspace.py` compose the existing plan/audition/assemble/
   key-art/report arms. The binding keeps stable ADO GUID, current display name
   and durable artifact namespace separate. State/input paths cannot escape the
   selected home, and child-only configuration does not rewrite the shared `.env`.
6. **Board isolation and discovery.** Bound board writes reject foreign production
   deliverables. The catalog includes projects with the production Shot type,
   not the engine's Scrum project. Existing unbound entry points remain available.
7. **Private-state recovery.** Fourteen identified text/state files were copied
   into their owning production homes with source/hash provenance. Original files,
   media bytes and refs remained intact. No active cast or approval was inferred.

The live review found three production projects, 22 work items, no production
wikis and three empty production Git repositories. Those are assessment-time
facts, not a substitute for querying the current board. The repositories were not
populated with engine copies. Different department coverage and missing Cut
instances were recorded, not silently healed.

## Delivery trail and evidence

All work-item numbers here belong to the engine's tracking project, not the
sibling organization. Resolve its concrete project/repository from the private
governing studio registry.

Epic #32 > Feature #33 > PBI #34 > criterion-mapped Tasks:

| Task | Commit | Result |
|---|---|---|
| #35 | `34d4be5` | Reusable administration MCP and skill |
| #36 | `8896555` | Engine delivery/mirror workflow |
| #37 | `8b90d7b` | Private production-home shape and onboarding templates |
| #38 | `2ba6d4e` | Explicit project-bound execution and production-only catalog |
| #39 | `914bcaf` | Isolation/continuity evidence, namespace regression guard and docs |
| #40 | This handoff commit | Complete session record and clean canonical-checkout cutover |

One branch/ADO PR serves the PBI, with one commit per Task. Commit bodies end in
the Task's `#<id>` directly below the change bullets, without author/session
trailers. Squash completion keeps individual Task evidence in the PR and uses
separate work-item-reference lines in the squash message.

All 14 Python smoke-test modules passed from a clean staged snapshot independent
of pre-existing WIP. Eight MCP behavior/protocol checks, five scoped startup cases,
native instruction discovery, live production-only enumeration and matching
ADO/GitHub branch heads were also checked. Production process IDs, imported-file
hashes and the original output-store junction were unchanged.

The apparent 10K-file change count was generated Node dependencies, not source
changes. `node_modules` is ignored and excluded from editor views/watchers; its
lockfile is tracked. Recreate dependency environments in a clone, not by moving
the old `.venv`.

## Pending work deliberately excluded from the new baseline

There were 16 pre-existing modified files when this effort began. They covered
casting-round/state refinements, rejected/approved-tag adjudication, post-casting
key-art conditioning/gating, portable delegated Graph authentication, supporting
exports/configuration and tests. They were not authored, committed or published
as part of this refactor. Their change payload was checked against the preserved
baseline after the five implementation commits.

The user's final direction is to establish a **clean** baseline and revisit
production-level work deliberately, rather than port those experiments. Keep the
legacy checkout and its recovery snapshot; do not silently delete it or apply its
patch to the canonical checkout.

Two implications are important:

- The old local configuration selected Graph storage with `GRAPH_AUTH=graph-cli`.
  That delegated-auth helper was in the excluded WIP, not the merged baseline.
  Restoring local pointers does **not** prove that this experimental auth mode
  works in the clean checkout. Validate/configure supported Graph authentication
  before live Graph operations; do not hide failure by silently switching stores.
- A Done casting item is not necessarily a Producer approval: some live candidates
  were tagged rejected. The excluded adjudication refinement must not be assumed
  present. Read explicit board verdicts/comments through MCP and ask the Producer
  before selecting or advancing; do not trust legacy report status alone.

The 0062 slot remains unwritten because its references belonged to that legacy
pending work. Do not fabricate a historical entry to fill the numbering gap.

## Approved post-merge canonical-checkout procedure

1. Complete the approved ADO PR by squash, without bypassing policies or casting
   approval votes on the user's behalf. Keep the final Task open until cutover
   evidence is recorded.
2. Clone merged `main` from ADO to the requested projects location, with the local
   directory named `sequiturstudiosystem`. Keep the old repository/workspace
   directories for recovery and session-history access.
3. Configure the clean clone's ADO primary and existing GitHub mirror; update the
   mirror's `main` and clean up the completed source branch. Preserve a local
   legacy recovery reference if its dirty checkout still occupies that branch.
4. Restore private runtime pointers only as ignored local configuration, attach
   the existing durable media store without copying/moving its bytes, and recreate
   Python/Node dependency environments. Do not port the 16 experimental edits or
   publish ignored source corpora, configuration, state or media.
5. Update only **active** engine registry, workspace, agent/skill, MCP and startup
   references. Add the canonical engine as its own engineering workspace root;
   productions remain peers beneath their Studios organization root, not children
   beneath the engine. Preserve historical import/snapshot source paths.
6. Verify clean Git state and merged commit identity, scoped startup, production
   bindings, dependency ignores, media linkage and the engine/production process
   distinction. Record actual paths, merge/clone identities and any runtime
   limitations in the private cutover report and on the PBI.

## Starting the next agent handoff

Read this entry, 0063, `context\production-workspaces.md` and
`context\git-workflow.md`. Then read the governing workspace's shared instructions,
matching organization profile and selected project's own context. Retrieve the
current ADO work items/PR/wiki rather than treating this snapshot as live state.

Use the studio registry for the canonical engine path and tracking home. Use a
production manifest for production work; never infer board identity from a folder
name or the engine's legacy `ADO_PROJECT` default.

Historical VS Code chats remain associated with their original workspace
identities. Nine matching stores, including older Studios paths, were backed up
with 39 chat files during the initial preservation pass. Those copies are not
native chat exports or session reassociation. A new clone is not a chat-history
transfer; leave original identities intact and use native export before any later
destructive cleanup.
