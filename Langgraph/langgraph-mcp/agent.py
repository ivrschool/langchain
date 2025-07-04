from typing import Annotated, Sequence, TypedDict, List
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, ToolMessage
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import Tool
from langgraph.graph import StateGraph, END
import asyncio


# Define agent state
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    number_of_steps: int

def create_react_agent(llm, tools: List[Tool]):
    tools_by_name = {tool.name: tool for tool in tools}
    model = llm.bind_tools(tools)

    async def call_tool(state: AgentState):
        outputs = []
        for tool_call in state["messages"][-1].tool_calls:
            tool = tools_by_name[tool_call["name"]]
            result = await tool.ainvoke(tool_call["args"])
            outputs.append(
                ToolMessage(
                    content=result,
                    name=tool_call["name"],
                    tool_call_id=tool_call["id"],
                )
            )
        return {"messages": outputs}

    async def call_model(state: AgentState, config: RunnableConfig):
        response = await model.ainvoke(state["messages"], config)
        return {"messages": [response]}

    def should_continue(state: AgentState):
        if not state["messages"][-1].tool_calls:
            return "end"
        return "continue"

    workflow = StateGraph(AgentState)

    workflow.add_node("llm", call_model)
    workflow.add_node("tools", call_tool)

    workflow.set_entry_point("llm")

    workflow.add_conditional_edges(
        "llm",
        should_continue,
        {
            "continue": "tools",
            "end": END,
        },
    )

    workflow.add_edge("tools", "llm")

    return workflow.compile()
