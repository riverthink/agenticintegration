import httpx, uvicorn
from uuid import uuid4
from a2a.server.apps import A2AStarletteApplication
from a2a.server.agent_execution import AgentExecutor
from a2a.server.events import EventQueue
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard
from a2a.utils import new_agent_text_message
from a2a.client import ClientFactory, ClientConfig
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import MessagesState, StateGraph

HTTP = httpx.AsyncClient(); B_URL = "http://localhost:9998"
async def call_agent_b(text: str) -> str:
    client_config = ClientConfig(httpx_client=HTTP, streaming=False)
    client = await ClientFactory.connect(
        agent=B_URL, client_config=client_config
    )
    print(f"Connected to Agent B at {B_URL}")
    message = {
        "role": "user",
        "parts": [{"kind": "text", "text": text}],
        "messageId": uuid4().hex,
    }
    result = None
    async for chunk in client.send_message(message):
        result = chunk
    return result.parts[0].root.text


def create_graph():
    async def process(state):
        text = state["messages"][-1].content
        reply = await call_agent_b(text)
        return {"messages": state["messages"] + [AIMessage(content=f"A got reply from B: {reply}")]}
    workflow = StateGraph(MessagesState)
    workflow.add_node("process", process)
    workflow.set_entry_point("process")
    workflow.set_finish_point("process")
    return workflow.compile()

graph = create_graph()


class A(AgentExecutor):
    async def execute(self, ctx, q: EventQueue):
        result = await graph.ainvoke({"messages": [HumanMessage(content=ctx.get_user_input())]})
        await q.enqueue_event(new_agent_text_message(result["messages"][-1].content))
        print("Second message enqueued")

    async def cancel(self, ctx, q):
        raise RuntimeError()


card = AgentCard(
    name="AgentA",
    description="Delegates to B",
    url="http://localhost:9999/",
    version="0.1",
    default_input_modes=["text"],
    default_output_modes=["text"],
    capabilities=AgentCapabilities(streaming=True),
    skills=[],
)

app = A2AStarletteApplication(card, DefaultRequestHandler(A(), InMemoryTaskStore())).build()
uvicorn.run(app, host="0.0.0.0", port=9999)

