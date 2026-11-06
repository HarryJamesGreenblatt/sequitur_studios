# Engine Delivery

The shared engine has one Git history: ADO Git is the primary repository and PR
home; the existing public GitHub repository is its mirror. The local `ado` remote
addresses the engine's private ADO repository. `origin` keeps its GitHub fetch URL
and has both GitHub and ADO push URLs.

Productions remain separate ADO projects on their production process. Their
briefs, casting state, private context and output do not belong in this engine's
public repository. A production workspace is not an engine fork or GitHub mirror.

## Work And Commits

Engine development uses its own Scrum project:

1. Epic groups Features; Feature groups PBIs.
2. Each PBI has ordered acceptance criteria, with one Task per criterion.
3. Use one branch and ADO PR per PBI, and one commit per Task.
4. Commit subjects use `type: Title Case Summary`, followed by a blank line,
   `- ` change bullets and the Task's `#<id>` directly below the last bullet.
   Additional IDs each get their own line. Do not add author/session trailers.
5. Link the PBI and Tasks to the PR, record evidence, and update their states as
   criteria are met. Do not include unrelated pending work in a Task's commit.

PR titles use `<Project>: Title Case`. Descriptions contain
`# Pull Request <id> - <title>`, `## Overview`, `## File Changes` with a fenced
diff-stat, and `## History` with the PBI and Task references.

## Authentication And Publishing

Use the configured organization-scoped MCP for ADO metadata, work items and PRs.
The administration companion supplies missing project/repository operations;
authentication is the caller's existing Entra identity, not a stored PAT.

Where Git Credential Manager has not signed into the engine organization, the
Git transport helper can reuse that identity without storing or printing tokens:

```powershell
node tools\ado-admin-mcp\git.mjs <organization> . push origin <branch>
```

Its temporary authorization header is scoped to the selected ADO organization,
not sent to the GitHub mirror, and not written into Git configuration.

For a fresh checkout, install the companion's locked dependencies with
`npm ci --prefix tools\ado-admin-mcp --ignore-scripts`. Keep `node_modules`
ignored; the lockfile is tracked so installations are repeatable.

Review the staged diff before publishing. Squash and delete a PR's source branch
only after approval; then update local `main` from `ado` and push it to `origin`.
