# Production Workspace Boundaries

The studio owns shared behavior; a production owns its state. This preserves the
engine/instance decisions in storyline 0005 and 0008 while giving each production
an actual local home.

```text
<studios-organization>\
  .github\                  Studio-wide instructions and shared-tool discovery
  context\                  Studio/engine index, not merged production history
  <production>\
    production.json         Explicit ADO identity and existing artifact namespace
    .github\                Project-local instructions
    context\                Brief, provenance and project decision history
    inputs\                 This production's source inputs
    state\                  This production's persistent local state
    .local\scratch\          Disposable, project-scoped render intermediates
```

The shared engine remains one repository with an ADO primary and GitHub mirror.
Production homes are private content workspaces, not engine clones, GitHub mirrors
or new Git repositories. Existing ADO production projects retain their custom
process independently of the engine project's Scrum process.

`templates\production` supplies an onboarding shape. Replace every placeholder
using live project metadata. The manifest's project GUID is stable identity;
its project name is the current display/area-path name. The artifact namespace
keeps existing output keys stable even if a local folder is renamed.

Keep existing media in its durable store. Copy only identified inputs and state
into the correct project home, record source paths and hashes, and preserve the
originals until a separate reviewed migration. Historical casting files are
archives, not automatically selected active state.

Never copy the shared engine devlog into every production. Its role/renderer/
provider decisions remain shared context; a production's brief and creative
decisions remain that project's context and ADO records.

## Bound Execution

Run shared arms from a private production home using its manifest:

```powershell
<engine-python> <engine-root>\scripts\production_workspace.py --project-root . plan "A premise" --dry-run
<engine-python> <engine-root>\scripts\production_workspace.py --project-root . audition --cast inputs\cast_spec.json
```

Actions are `plan`, `audition`, `assemble`, `key-art` and `report`. They compose the
existing execution arms rather than copying the crew or its film logic. Use
`--print-command` before the action to inspect the binding without executing it.
In a project-scoped session, `SEQUITUR_PROJECT_ROOT` supplies the selected home.

Input/state/output path arguments must remain inside that home. The audition
default is `state\cast.json`; selecting an archived state requires an explicit
`--state state\legacy\<file>.json`. Render intermediates use `.local\scratch`.
The shared engine `.env` is not rewritten: child-only settings bind the selected
board GUID, current display name, durable artifact namespace and scratch root.

Bound board writes reject deliverables from another production. Unbound legacy
entry points retain their explicit-project/default behavior. Production discovery
includes only projects with the Shot work-item type, so the engine's engineering
project is not offered as a film production.
