import assert from "node:assert/strict";
import test from "node:test";
import { Administration } from "./administration.mjs";

const template = { id: "scrum-id", name: "Scrum" };
const existing = {
  id: "project-id",
  name: "Engine",
  visibility: 0,
  capabilities: { processTemplate: { templateTypeId: template.id } },
};

function fixture(core = {}, git = {}) {
  return new Administration(async () => ({
    getCoreApi: async () => ({ getProcesses: async () => [template], ...core }),
    getGitApi: async () => git,
  }));
}

test("project creation resolves the selected process and never changes other projects", async () => {
  let created;
  const admin = fixture({
    getProject: async () => { throw Object.assign(new Error("not found"), { statusCode: 404 }); },
    queueCreateProject: async (value) => { created = value; return { id: "operation" }; },
  });
  const result = await admin.createProject({ name: "Engine", process: "Scrum" });
  assert.equal(result.provisioning, "queued");
  assert.equal(created.visibility, 0);
  assert.equal(created.capabilities.processTemplate.templateTypeId, template.id);
  assert.equal(created.capabilities.versioncontrol.sourceControlType, "Git");
});

test("an existing matching project is reused without mutation", async () => {
  const admin = fixture({ getProject: async () => existing });
  assert.equal((await admin.createProject({ name: "Engine", process: "Scrum" })).created, false);
});

test("an existing production on another process is not converted", async () => {
  const admin = fixture({
    getProject: async () => ({
      ...existing,
      capabilities: { processTemplate: { templateTypeId: "production-process" } },
    }),
  });
  await assert.rejects(admin.createProject({ name: "Film", process: "Scrum" }), /not changed/);
});

test("authentication errors are not mistaken for an absent project", async () => {
  const denied = Object.assign(new Error("forbidden"), { statusCode: 403 });
  const admin = fixture({ getProject: async () => { throw denied; } });
  await assert.rejects(admin.createProject({ name: "Engine", process: "Scrum" }), denied);
});

test("an unknown process fails before attempting a project write", async () => {
  const admin = fixture();
  await assert.rejects(admin.createProject({ name: "Engine", process: "Missing" }), /not found/);
});

test("repository creation binds to the resolved project and is repeatable", async () => {
  let calls = 0;
  const repositories = [];
  const admin = fixture(
    { getProject: async () => existing },
    {
      getRepositories: async () => repositories,
      createRepository: async (body, project) => {
        calls++;
        assert.equal(project, existing.id);
        assert.equal(body.project.id, existing.id);
        const repository = { id: "repo", name: body.name };
        repositories.push(repository);
        return repository;
      },
    },
  );
  assert.equal((await admin.createRepository({ project: "Engine", name: "engine" })).created, true);
  assert.equal((await admin.createRepository({ project: "Engine", name: "engine" })).created, false);
  assert.equal(calls, 1);
});

test("repository update refuses a stale identity or a missing default branch", async () => {
  const admin = fixture({}, {
    getRepository: async () => ({ id: "repo", name: "engine" }),
    getRefs: async () => [{ name: "refs/heads/main" }],
  });
  await assert.rejects(
    admin.updateRepository({ project: "Engine", repository: "repo", expectedName: "old", name: "new" }),
    /identity changed/,
  );
  await assert.rejects(
    admin.updateRepository({
      project: "Engine", repository: "repo", expectedName: "engine",
      defaultBranch: "refs/heads/missing",
    }),
    /does not exist/,
  );
});
