# main.py

import asyncio
import os
from langgraph_sdk import get_client
from langgraph_sdk.schema import Checkpoint
from dotenv import load_dotenv
import httpx

load_dotenv()

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_ANON_KEY = os.environ["SUPABASE_ANON_KEY"]

# print(SUPABASE_URL)
# print(SUPABASE_ANON_KEY)

async def login(email: str, password: str) -> str | None:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{SUPABASE_URL}/auth/v1/token?grant_type=password",
            json={"email": email, "password": password},
            headers={
                "apikey": SUPABASE_ANON_KEY,
                "Content-Type": "application/json"
            },
        )
        if response.status_code != 200:
            print("❌ Login failed:", response.text)
            return None
        return response.json()["access_token"]

async def run_chat():
    email = input("📧 Email: ")
    password = input("🔐 Password: ")
    token = await login(email, password)

    if not token:
        print("🚫 Login failed. Cannot start chat.")
        return

    client = get_client(
        url="http://localhost:2024",  # must match your langgraph dev server
        headers={"Authorization": f"Bearer {token}"}
    )

    thread = await client.threads.create()

    while True:
        user_input = input("You: ")
        if user_input.strip().lower() == "exit":
            break

        response = await client.runs.wait(
            thread_id=thread["thread_id"],
            assistant_id="agent",
            input={"messages": [{"role": "user", "content": user_input}]},
            config={"configurable": {"recursion_limit": 50 }},
      
          
        )
        reply = response["messages"][-1]["content"]
        print("Agent:", reply, "\n")

asyncio.run(run_chat())
