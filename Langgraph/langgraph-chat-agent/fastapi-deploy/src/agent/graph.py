# src/agent/graph.py

import os
from dotenv import load_dotenv
from psycopg_pool import AsyncConnectionPool
from langgraph.graph import StateGraph, END, MessagesState
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langchain_core.messages import AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

DB_URI = os.getenv("DB_URI", "postgresql://postgres:example@localhost:5432/postgres?sslmode=disable")
connection_kwargs = {
    "autocommit": True,
    "prepare_threshold": 0,
}

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

async def chat_node(state: MessagesState):
    message = state["messages"]
    response = await llm.ainvoke(message)
    return {"messages": [AIMessage(content=response.content)]}

async def build_graph():
    pool = AsyncConnectionPool(DB_URI, kwargs=connection_kwargs)
    checkpointer = AsyncPostgresSaver(pool)
    await checkpointer.setup()

    graph_builder = StateGraph(MessagesState)
    graph_builder.add_node("chat", chat_node)
    graph_builder.set_entry_point("chat")
    graph_builder.set_finish_point("chat")

    return graph_builder.compile(checkpointer=checkpointer)
