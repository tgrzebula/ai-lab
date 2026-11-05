# MCP intro (2026)

My part of the exercises from
[Introduction to Model Context Protocol](https://anthropic.skilljar.com/introduction-to-model-context-protocol/296694)
(Anthropic Academy): an MCP server exposing a small in-memory document store, and the
client methods that talk to it from a CLI chat app.

The course provides the app skeleton (CLI, chat loop, Claude wrapper, client
connection code) and sample data. That part is Anthropic's and is not published here,
so this folder does not run on its own — the full working project is in the course.

| File | What it is |
|------|------------|
| `mcp_server.py` | FastMCP server: tools `read_doc_contents` and `edit_document`, resources `docs://documents` and `docs://documents/{doc_id}`, prompt `format`. Header comment marks the starter lines |

The summarize prompt was left as a TODO.

## Client side

The course's `MCPClient` class comes with the connection handled and the protocol
methods empty. These are my implementations:

```python
async def list_tools(self) -> list[types.Tool]:
    result = await self.session().list_tools()
    return result.tools

async def call_tool(self, tool_name: str, tool_input: dict) -> types.CallToolResult | None:
    return await self.session().call_tool(tool_name, tool_input)

async def list_prompts(self) -> list[types.Prompt]:
    result = await self.session().list_prompts()
    return result.prompts

async def get_prompt(self, prompt_name, args: dict[str, str]):
    result = await self.session().get_prompt(prompt_name, args)
    return result.messages

async def read_resource(self, uri: str) -> Any:
    result = await self.session().read_resource(AnyUrl(uri))
    resource = result.contents[0]
    if isinstance(resource, types.TextResourceContents):
        if resource.mimeType == "application/json":
            return json.loads(resource.text)
    return resource.text
```

Each one is a thin pass-through to `ClientSession`. The only logic is in
`read_resource`, which decodes JSON when the server declares that MIME type — that is
how the list of document IDs arrives as a Python list rather than a string.

## Stack

Python, `mcp` (FastMCP, `ClientSession` over stdio), Anthropic API.
