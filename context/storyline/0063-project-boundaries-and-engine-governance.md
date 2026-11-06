# 0063 — Project boundaries and engine governance

> Date: 2026-11-05 · Focus: distinguish the shared studio system from its production
> instances, establish the engine's delivery workflow, and complete the local
> per-production boundary without moving historical repository/session paths.

The 0062 slot was already referenced by pending casting/key-art work when this
refinement started. That uncommitted work and its numbering were not reassigned.

## What happened

The first governing-workspace bootstrap provided routing and navigation but still
presented the engine as if it were the parent production. The historical decisions
already said otherwise: 0005 separates code from content, and 0008 separates shared
role behavior from per-production state. The missing piece was a consistent local
binding, not a new film hierarchy or a fork of the engine for every production.

The studio now has peer private production homes, each with its own instructions,
context, inputs, state and manifest. Identified historical text/state files were
copied with source/hash provenance; originals and durable media remain intact.
No cast selection or approval was inferred during import.

The engine has a dedicated ADO Git/engineering home with a GitHub mirror. It uses
Scrum for its own development; existing productions retain their custom process.
Project-scoped process selection does not imply changing an organization's other
projects.

## Decisions

1. **Publish the reusable studio, not its productions.** One shared engine
   repository; production homes are private ADO-managed content instances, not
   engine forks or GitHub mirrors.
2. **Bind identity once.** A local manifest records the stable ADO project GUID,
   current display name, owning organization and existing artifact namespace.
3. **Reuse existing arms.** The workspace runner composes plan, audition, assemble,
   key-art and report commands, supplying child-only configuration and scoped
   input/state/scratch paths instead of duplicating film logic.
4. **Fail before a foreign write.** Bound execution rejects production overrides,
   escaping project-owned paths and a deliverable for another production.
5. **Keep engineering out of the production catalog.** Discovery includes projects
   with the production Shot type, not every project in a mixed-purpose organization.
6. **Extend MCP, not shell workarounds.** A typed companion provides missing
   process/project/repository administration, with no arbitrary request, deletion
   or process-conversion operation.
7. **Preserve pending work.** Task-mapped commits contain only this refinement;
   earlier uncommitted engine changes remain unstaged and unpublished.

## Resulting state

See `context\production-workspaces.md` for the local boundary/runner and
`context\git-workflow.md` for Epic → Feature → PBI → Task → commit delivery.
The existing engine/provider/store seams remain intact, with project-bound mode
added alongside legacy unbound calls.

## Open threads

- Resume a historical casting state only after the Producer explicitly identifies
  the state/selection to use; copied files are not approval evidence.
- Physical relocation and VS Code session reassociation remain separate migration
  work. Existing workspaces and session stores stay at their original identities.
