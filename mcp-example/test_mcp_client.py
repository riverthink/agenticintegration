import json
import anyio
from langchain_openai import ChatOpenAI
from mcp import ClientSession
from mcp.client.sse import sse_client

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

async def pick_tool(tools, question: str) -> tuple[str, dict]:
    specs = [
        {"name": t.name, "description": t.description, "inputSchema": t.inputSchema}
        for t in tools
    ]
    prompt = (
        "Pick the single best tool and JSON args. Infer values from the request.\n"
        f"Tools: {json.dumps(specs)}\n"
        'Return JSON only, e.g., {"tool": "get_weather", "arguments": {"city": "Paris"}}.\n'
        f"User: {question}"
    )
 
    parsed = json.loads((await llm.ainvoke(prompt)).content)
    tool, args = parsed.get("tool"), parsed.get("arguments") or {}
    print("Picked tool:", tool, args)
    return tool, args

async def main() -> None:
    # Connect to the SSE endpoint
    sse_url = "http://127.0.0.1:8000/sse"
    
    async with sse_client(sse_url) as (r, w):
        async with ClientSession(r, w) as session:
            await session.initialize()
            tools = (await session.list_tools()).tools
            print("Available tools:")
            for t in tools:
                print(f"- {t.name}: {t.description}")
            question = await anyio.to_thread.run_sync(input, "What do you need? ")
            tool, args = await pick_tool(tools, question)
            result = await session.call_tool(tool, args)
            print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    anyio.run(main)
    
    