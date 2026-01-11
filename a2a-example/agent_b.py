import uvicorn
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.server.agent_execution import AgentExecutor
from a2a.server.events import EventQueue
from a2a.types import AgentCard, AgentCapabilities
from a2a.utils import new_agent_text_message
from langgraph.graph import StateGraph, MessagesState
from langchain_core.messages import HumanMessage, AIMessage


def create_graph():
    workflow = StateGraph(MessagesState)
    workflow.add_node("process", lambda s: {
        "messages": s["messages"] + [AIMessage(content=f"Langgraph_B: {s['messages'][-1].content}")]
    })
    workflow.set_entry_point("process")
    workflow.set_finish_point("process")
    return workflow.compile()


graph = create_graph()


class B(AgentExecutor):
    async def execute(self, ctx, q: EventQueue): # Starts the task execution
        result = await graph.ainvoke({"messages": [HumanMessage(content=ctx.get_user_input())]})
        await q.enqueue_event(new_agent_text_message(result["messages"][-1].content)) # Send the response back to the user from Agent B to Agent A

    async def cancel(self, ctx, q):
        raise RuntimeError()


card = AgentCard(
    name="AgentB", description="LangGraph agent", url="http://localhost:9998/",
    version="0.1", default_input_modes=["text"], default_output_modes=["text"],
    capabilities=AgentCapabilities(streaming=True), skills=[]
)

app = A2AStarletteApplication(card, DefaultRequestHandler(B(), InMemoryTaskStore())).build()
uvicorn.run(app, host="0.0.0.0", port=9998)
