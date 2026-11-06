---
name: ado-administration
description: >-
  Use for Azure DevOps project/repository provisioning or project metadata/process
  inspection that the stock ADO MCP does not expose. Uses the organization-scoped
  companion administration MCP; never substitutes shell REST for conversational
  administration.
---
# ADO Administration

1. Resolve the organization and project explicitly from the governing workspace.
   Use its matching organization-scoped administration connection. No
   cross-organization fallback.
2. Read current project metadata with `admin_project_get` and available templates
   with `admin_process_list`. Do not infer the process from the organization name:
   the engine's Scrum process and each production's custom process are independent.
3. Before writes, confirm the requested project/repository names, private
   visibility and process. Never change an existing production's process to make
   an engine-administration operation succeed.
4. `admin_project_create` resolves a named existing process and returns either the
   matching project or a queued creation. A queued operation is not completion:
   wait and retrieve the project until it is ready; report failures explicitly.
5. Use `admin_repository_create` for a new repository, or
   `admin_repository_update` with its exact expected current name for a deliberate
   rename. A default branch can be selected only after that branch exists.
6. Use the stock ADO MCP for work items, wiki and PR operations after provisioning.
   Record the engine work on its Scrum board; productions retain their own boards.
7. Check the resulting project ID, process ID, repository ID and remote URL before
   changing local Git configuration. Never force-push, publish production content
   to GitHub, or include local secrets in a commit.

The companion lives at `tools\ado-admin-mcp` in the shared engine repository.
It uses the Azure DevOps SDK and Azure CLI identity behind typed MCP tools. It has
no arbitrary URL/request operation, deletion operation or process-conversion tool.
Do not modify the npm-cached Microsoft MCP package.
