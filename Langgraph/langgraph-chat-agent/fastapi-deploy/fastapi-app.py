# app.py

import os
import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from src.agent.graph import build_graph  # Import the async builder

load_dotenv()

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_SERVICE_KEY = os.environ["SUPABASE_SERVICE_KEY"]

app = FastAPI()
security = HTTPBearer()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    token = credentials.credentials
    headers = {
        "Authorization": f"Bearer {token}",
        "apiKey": SUPABASE_SERVICE_KEY,
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SUPABASE_URL}/auth/v1/user", headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        return response.json()

class ChatRequest(BaseModel):
    message: str
    thread_id: str | None = None

@app.post("/chat")
async def invoke_chat(request: ChatRequest, user=Depends(get_current_user)):
    """Run LangGraph with async Postgres checkpointer."""
    graph = await build_graph()
    config = {
        "configurable": {
            "user_id": user["id"],
            "thread_id": user["id"],  # Use user ID as thread identifier
            "checkpoint_ns": "chat_session"
        }
    }
    print(request.thread_id, user["id"])

    result = await graph.ainvoke({"messages": [HumanMessage(content=request.message)]}, config=config)
    return result["messages"][-1]
