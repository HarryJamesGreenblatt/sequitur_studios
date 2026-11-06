# Sequitur Studios Engine Instructions

This repository is the singular studio engine, not a production-specific fork.
It models film-craft seats and an interactive Producer-led production pipeline.

## Scope And Bootstrap

- When opened through the governing Sequitur workspace, read its shared
  instructions, the matching Studios organization profile and its project registry.
  Do not assume arbitrary parent instructions are automatically included.
- Outside that workspace, identify the owning organization from the local MCP
  configuration and explicitly select the target production/project. If the
  connection or project is unresolved, report it before ADO work.
- Studio engine work and production work use the Studios organization, never the
  sibling Scrum organization. The engine's own project uses Scrum; follow
  `context\git-workflow.md` and the Epic > Feature > PBI > Task > commit chain.
  Production projects retain their custom film-production process.
- Resolve the engine's tracking project from the governing studio registry, not
  from the application's `ADO_PROJECT` default. Ask if that tracking home is
  unresolved in a standalone checkout.
- Local infrastructure identifiers belong in local configuration, not public
  documentation. Keep secrets and excluded source material out of commits.

## Read Before Working

- Read `context\architecture.md` for the domain/runtime architecture.
- Read `context\storyline\OVERVIEW.md` and the relevant recent numbered entries
  for decisions; verify current behavior in code and the selected live board.
- Keep numbered storyline entries as history. Update current documentation for
  actual changes without treating an old "next" paragraph as authoritative scope.
- Retrieve the selected production's work items, approved reports and wiki before
  production changes. Board operations use MCP; an unavailable connection is a
  blocker, not permission to query another organization's board.

## Preserve The Model

- `sequitur\crew` holds craft roles and owned vocabularies; Director reconciles,
  the human Producer approves, and the engine dispatches.
- `.github\agents` holds creative personas and `.github\skills` execution arms.
  Read the applicable persona/skill before invoking that creative workflow.
- Preserve the provider/output-store seams, the separate decision/execution
  planes, and phase gates. Never render before the required human greenlight.
- Persist/report deliverables incrementally with visible failures and reconcile
  as needed; do not claim approval until its verdict is actually recorded.
- Follow existing Python patterns and focused tests in `tests`. Run the relevant
  existing tests for behavior changes; do not add tooling just for alignment.
- Preserve existing dirty work, remotes, private configuration, ignored grounding
  sources and the output-store link. No physical migration is implied here.

## Production Boundaries

- Read `context\production-workspaces.md`. Production-owned instructions, context,
  inputs and state live in peer project homes, not under an Engine production.
- Execute production arms through `scripts\production_workspace.py` with an
  explicit project root, or within a session launched for that production.
  The manifest owns the ADO GUID and artifact namespace; do not override it.
- Keep media refs stable and private project content outside the published engine.
  Imported cast files are historical alternatives, not an automatically active cast.
