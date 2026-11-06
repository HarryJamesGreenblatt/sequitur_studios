import { AzureCliCredential } from "@azure/identity";
import { spawnSync } from "node:child_process";

const [organization, repository, operation, ...arguments_] = process.argv.slice(2);
if (!organization || !/^[a-zA-Z0-9][a-zA-Z0-9-]*$/.test(organization)) {
  throw new Error("Supply one Azure DevOps organization.");
}
if (!repository || !["ls-remote", "push", "fetch"].includes(operation)) {
  throw new Error("Supply a local repository and a Git transport operation.");
}
const token = await new AzureCliCredential().getToken(
  "499b84ac-1321-427f-aa17-267ca6975798/.default",
);
if (!token?.token) throw new Error("Azure DevOps authentication returned no token.");
const environment = { ...process.env };
const index = Number.parseInt(environment.GIT_CONFIG_COUNT ?? "0", 10);
if (!Number.isSafeInteger(index) || index < 0) throw new Error("Invalid Git environment configuration.");
environment.GIT_CONFIG_COUNT = String(index + 1);
environment[`GIT_CONFIG_KEY_${index}`] =
  `http.https://dev.azure.com/${organization}/.extraheader`;
environment[`GIT_CONFIG_VALUE_${index}`] = `AUTHORIZATION: bearer ${token.token}`;
environment.GIT_TERMINAL_PROMPT = "0";
environment.GCM_INTERACTIVE = "Never";

const result = spawnSync("git", ["-C", repository, operation, ...arguments_], {
  env: environment,
  stdio: "inherit",
});
if (result.error) throw result.error;
process.exitCode = result.status ?? 1;
