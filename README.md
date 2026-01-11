# Agentic Integration Examples

This repository demonstrates two key integration patterns for agentic systems:

1. **Agent-to-Agent (A2A) Communication** - How agents can communicate and delegate tasks to each other
2. **Model Context Protocol (MCP)** - How agents can access external tools and data sources

## Project Structure

```
.
├── a2a-example/          # Agent-to-Agent communication examples
│   ├── agent_a.py        # Agent A that delegates to Agent B
│   ├── agent_b.py        # Agent B that processes requests
│   ├── test_a2a_curl.sh  # Test script using curl
│   ├── agents_sequence_conceptual.mmd  # Conceptual sequence diagram
│   └── agents_sequence_logical.mmd     # Logical sequence diagram
│
└── mcp-example/          # Model Context Protocol examples
    ├── mcp_sse_server.py      # MCP server with weather/traffic tools
    ├── test_mcp_client.py     # MCP client with LLM tool selection
    └── mcp_sequence.mmd       # MCP sequence diagram
```

## A2A Example: Agent-to-Agent Communication

The A2A example demonstrates how two agents can communicate using the Agent-to-Agent protocol with LangGraph workflows.

### Architecture

- **Agent A** (port 9999): Receives user requests and delegates to Agent B
- **Agent B** (port 9998): Processes requests and returns responses
- Both agents use LangGraph for workflow orchestration
- Communication happens via the A2A protocol over HTTP

### Running the Example

1. Install dependencies:
```bash
pip install a2a-sdk langgraph langchain-core httpx uvicorn
```

2. Start Agent B (in one terminal):
```bash
cd a2a-example
python agent_b.py
```

3. Start Agent A (in another terminal):
```bash
cd a2a-example
python agent_a.py
```

4. Test with curl:
```bash
./test_a2a_curl.sh
```

### How It Works

1. Agent A exposes an A2A endpoint and creates a LangGraph workflow
2. When a message arrives, Agent A's workflow calls Agent B via the A2A client
3. Agent B processes the request through its LangGraph workflow
4. Agent B returns the response to Agent A
5. Agent A combines the response and returns it to the original caller

## MCP Example: Model Context Protocol

The MCP example demonstrates how to create a tool server and have an LLM-powered client intelligently select and use tools.

### Architecture

- **MCP Server** (port 8000): Exposes weather and traffic data tools via Server-Sent Events (SSE)
- **MCP Client**: Connects to the server, uses GPT-4 to select appropriate tools based on user questions

### Running the Example

1. Install dependencies:
```bash
pip install mcp fastmcp langchain-openai uvicorn anyio
```

2. Set your OpenAI API key:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

3. Start the MCP server (in one terminal):
```bash
cd mcp-example
python mcp_sse_server.py
```

4. Run the client (in another terminal):
```bash
cd mcp-example
python test_mcp_client.py
```

5. Ask questions like:
   - "What's the weather in Paris?"
   - "How's traffic on Highway 101?"

### How It Works

1. The MCP server exposes two tools: `get_weather` and `get_traffic`
2. The client connects via SSE and lists available tools
3. When the user asks a question, the LLM analyzes the question and available tools
4. The LLM selects the best tool and generates appropriate arguments
5. The client calls the selected tool and displays the results

## Key Technologies

- **A2A SDK**: Protocol for agent-to-agent communication
- **LangGraph**: Framework for building stateful agent workflows
- **FastMCP**: Fast implementation of the Model Context Protocol
- **LangChain**: Framework for building LLM applications
- **Uvicorn**: ASGI server for running async Python web apps

## Use Cases

### A2A Pattern
- Building multi-agent systems where agents specialize in different tasks
- Creating agent pipelines and workflows
- Enabling agents to delegate complex tasks to specialized agents

### MCP Pattern
- Giving agents access to external data sources
- Enabling tool use with intelligent tool selection
- Building extensible agent systems with pluggable capabilities

## Testing with MCP Inspector

You can also test the MCP server using the official MCP inspector:

```bash
npx @modelcontextprotocol/inspector
```

Then connect to `http://127.0.0.1:8000/sse`

## License

MIT
