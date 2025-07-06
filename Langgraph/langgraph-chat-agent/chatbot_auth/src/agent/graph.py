# src/agent/graph.py

from langgraph.graph import StateGraph, END, MessagesState

from dotenv import load_dotenv
load_dotenv()


from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

def chat_node(state: MessagesState):
    message = state.get("messages")
    response = llm.invoke(message)
    return {"messages": [{"role": "assistant", "content": f"{response.content}"}]}

graph_builder = StateGraph(MessagesState)
graph_builder.add_node("chat", chat_node)
graph_builder.set_entry_point("chat")
graph_builder.set_finish_point("chat")
graph = graph_builder.compile()
