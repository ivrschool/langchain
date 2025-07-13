# src/agent/graph.py

from langgraph.graph import StateGraph, END, MessagesState
import os
from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI

from langgraph.store.memory import InMemoryStore
from langgraph.store.postgres import PostgresStore
from langgraph.checkpoint.postgres import PostgresSaver
from psycopg import Connection
from psycopg_pool import ConnectionPool


DATABASE_URI = os.environ['DATABASE_URI']



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


connection_kwargs = {
    "autocommit": True,
    "prepare_threshold": 0,
}

with ConnectionPool(
    # Example configuration
    conninfo=DATABASE_URI,
    max_size=20,
    kwargs=connection_kwargs,
) as pool:
    checkpointer = PostgresSaver(pool)

    # NOTE: you need to call .setup() the first time you're using your checkpointer
    checkpointer.setup()

    graph_builder = StateGraph(MessagesState)
    graph_builder.add_node("chat", chat_node)
    graph_builder.set_entry_point("chat")
    graph_builder.set_finish_point("chat")
    graph = graph_builder.compile(checkpointer=checkpointer)