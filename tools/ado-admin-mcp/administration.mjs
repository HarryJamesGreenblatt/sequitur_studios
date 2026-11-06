export class Administration {
  constructor(connectionProvider) {
    this.connectionProvider = connectionProvider;
  }

  async processes() {
    const connection = await this.connectionProvider();
    return (await connection.getCoreApi()).getProcesses();
  }

  async project(project) {
    const connection = await this.connectionProvider();
    return (await connection.getCoreApi()).getProject(project, true, false);
  }

  async createProject({ name, process, description = "" }) {
    const connection = await this.connectionProvider();
    const core = await connection.getCoreApi();
    const processes = await core.getProcesses();
    const template = processes.find(
      (candidate) => candidate.name?.toLowerCase() === process.toLowerCase(),
    );
    if (!template?.id) {
      throw new Error(`Process '${process}' was not found. No project was created.`);
    }

    let existing;
    try {
      existing = await core.getProject(name, true, false);
    } catch (error) {
      if (error?.statusCode !== 404) throw error;
    }
    if (existing) {
      const actual = existing.capabilities?.processTemplate?.templateTypeId;
      if (actual?.toLowerCase() !== template.id.toLowerCase()) {
        throw new Error(
          `Project '${name}' already exists on another or unresolved process; it was not changed.`,
        );
      }
      if (existing.visibility !== 0 && existing.visibility !== "private") {
        throw new Error(`Project '${name}' is not private; it was not changed.`);
      }
      return { created: false, project: existing };
    }

    const operation = await core.queueCreateProject({
      name,
      description,
      visibility: 0,
      capabilities: {
        versioncontrol: { sourceControlType: "Git" },
        processTemplate: { templateTypeId: template.id },
      },
    });
    return { created: true, provisioning: "queued", operation };
  }

  async updateProject({ project, description }) {
    const connection = await this.connectionProvider();
    const core = await connection.getCoreApi();
    const existing = await core.getProject(project, true, false);
    const operation = await core.updateProject({ description }, existing.id);
    return { projectId: existing.id, operation };
  }

  async createRepository({ project, name }) {
    const connection = await this.connectionProvider();
    const core = await connection.getCoreApi();
    const owner = await core.getProject(project, true, false);
    const git = await connection.getGitApi();
    const repositories = await git.getRepositories(owner.id);
    const existing = repositories.find(
      (candidate) => candidate.name?.toLowerCase() === name.toLowerCase(),
    );
    if (existing) return { created: false, repository: existing };
    const repository = await git.createRepository(
      { name, project: { id: owner.id } },
      owner.id,
    );
    return { created: true, repository };
  }

  async updateRepository({ project, repository, expectedName, name, defaultBranch }) {
    if (name === undefined && defaultBranch === undefined) {
      throw new Error("Specify a repository name or default branch to update.");
    }
    const connection = await this.connectionProvider();
    const git = await connection.getGitApi();
    const existing = await git.getRepository(repository, project);
    if (existing.name !== expectedName) {
      throw new Error("Repository identity changed; no update was applied.");
    }
    const update = {};
    if (name !== undefined) update.name = name;
    if (defaultBranch !== undefined) {
      if (!defaultBranch.startsWith("refs/heads/")) {
        throw new Error("Default branch must use a refs/heads/ reference.");
      }
      const branches = await git.getRefs(existing.id, project, "heads/");
      if (!branches.some((branch) => branch.name === defaultBranch)) {
        throw new Error("The requested default branch does not exist.");
      }
      update.defaultBranch = defaultBranch;
    }
    return git.updateRepository(update, existing.id, project);
  }
}
