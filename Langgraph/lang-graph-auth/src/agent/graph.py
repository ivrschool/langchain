from langgraph.graph import StateGraph, END,  MessagesState
from langchain_core.runnables import RunnableLambda
from langchain_core.messages import HumanMessage
# Define simple echo node
def echo_node(state:  MessagesState):
    message = state.get("messages")[-1].content
    return {"messages": [{"role": "assistant", "content": f"You said: {message}"}]}

# Build the graph
graph_builder = StateGraph( MessagesState)
graph_builder.add_node("echo", RunnableLambda(echo_node))
graph_builder.set_entry_point("echo")
graph_builder.set_finish_point("echo")  # End after one response

graph = graph_builder.compile()
