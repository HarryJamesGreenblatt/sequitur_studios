import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";
import { fileURLToPath } from "node:url";

const [organization, tool, argumentsJson = "{}", mode = "admin"] = process.argv.slice(2);
if (!organization || !/^[a-zA-Z0-9][a-zA-Z0-9-]*$/.test(organization)) {
  throw new Error("Supply one organization, optional tool and JSON arguments.");
}
if (!["admin", "stock"].includes(mode)) throw new Error("Server mode must be admin or stock.");
const client = new Client({ name: "sequitur-admin-bootstrap", version: "0.1.0" });
const transport = new StdioClientTransport(mode === "admin" ? {
  command: process.execPath,
  args: [fileURLToPath(new URL("./server.mjs", import.meta.url)), organization],
  stderr: "inherit",
} : {
  command: process.env.ComSpec,
  args: [
    "/d", "/s", "/c",
    `npx --offline --no-install @azure-devops/mcp ${organization} --authentication azcli -d core work work-items search wiki repositories`,
  ],
  stderr: "inherit",
});
try {
  await client.connect(transport);
  const { tools } = await client.listTools();
  if (!tool) {
    console.log(JSON.stringify(tools, null, 2));
  } else {
    if (!tools.some((candidate) => candidate.name === tool)) {
      throw new Error(`Unknown administration MCP tool: ${tool}`);
    }
    const result = await client.callTool({ name: tool, arguments: JSON.parse(argumentsJson) });
    if (result.isError) {
      throw new Error(result.content.map((item) => item.text ?? "").join("\n"));
    }
    console.log(result.content.map((item) => item.text ?? "").join("\n"));
  }
} finally {
  await client.close();
}
