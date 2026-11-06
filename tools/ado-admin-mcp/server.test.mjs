import assert from "node:assert/strict";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

test("the real stdio server advertises typed, organization-scoped administration tools", async () => {
  const client = new Client({ name: "protocol-test", version: "1" });
  const transport = new StdioClientTransport({
    command: process.execPath,
    args: [fileURLToPath(new URL("./server.mjs", import.meta.url)), "example-org"],
    stderr: "inherit",
  });
  try {
    await client.connect(transport);
    const { tools } = await client.listTools();
    assert.equal(tools.length, 6);
    const create = tools.find((tool) => tool.name === "admin_project_create");
    assert.deepEqual(create.inputSchema.required, ["name", "process"]);
    assert.match(create.description, /example-org/);
    assert.equal(create.annotations.readOnlyHint, false);
    assert.ok(!tools.some((tool) => /delete|request|rest/i.test(tool.name)));
  } finally {
    await client.close();
  }
});
