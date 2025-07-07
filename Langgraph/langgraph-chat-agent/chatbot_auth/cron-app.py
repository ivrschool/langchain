# cron_app.py

import asyncio
import os
from dotenv import load_dotenv
from langgraph_sdk import get_client
import httpx

load_dotenv()

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_ANON_KEY = os.environ["SUPABASE_ANON_KEY"]
EMAIL = os.environ["CRON_USER_EMAIL"]
PASSWORD = os.environ["CRON_USER_PASSWORD"]

DEPLOYMENT_URL = "http://localhost:2024"
ASSISTANT_ID = "agent"
SCHEDULE = "17 05 * * *"  # Change this as needed

async def login(email: str, password: str) -> str | None:
    """Login and get access token."""
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

async def main():
    # token = await login(EMAIL, PASSWORD)
    # if not token:
    #     print("🚫 Cannot proceed without token.")
    #     return

    client = get_client(
        url=DEPLOYMENT_URL,
        # headers={"Authorization": f"Bearer {token}"}
    )

    thread = await client.threads.create()


    # cron_job = await client.crons.create_for_thread(
    #     thread_id=thread["thread_id"],
    #     assistant_id=ASSISTANT_ID,
    #     schedule=SCHEDULE,
    #     input={"messages": [{"role": "user", "content": "Run the daily task"}]},
    # )

    # Cron jobs are not supported in local LangGraph deployments
    # This feature is only available in LangGraph Cloud
    print("❌ Cron jobs are not supported in local deployments")
    print("🧵 Thread ID: {thread['thread_id']}")
    print("💡 Use LangGraph Cloud for cron job functionality")

if __name__ == "__main__":
    asyncio.run(main())
