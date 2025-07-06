# main.py

import asyncio
import os
import httpx
from dotenv import load_dotenv
from langgraph_sdk import get_client

load_dotenv()

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_ANON_KEY = os.environ["SUPABASE_ANON_KEY"]


async def sign_up(email: str, password: str):
    """Sign up a new user."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{SUPABASE_URL}/auth/v1/signup",
            json={"email": email, "password": password},
            headers={"apikey": SUPABASE_ANON_KEY},
        )
        if response.status_code != 200:
            print("❌ Signup failed:", response.text)
            return None
        print("✅ Signup successful! Please check your email to confirm before logging in.")
        return response.json()


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


async def run_chat(token: str):
    """Run the chatbot after successful login."""
    client = get_client(
        url="http://localhost:2024",
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
            config={"configurable": {"recursion_limit": 50}},
            checkpoint_during=True,
        )
        reply = response["messages"][-1]["content"]
        print("Agent:", reply, "\n")


async def main():
    print("👋 Welcome! Do you want to:")
    print("1. Login")
    print("2. Sign up")

    choice = input("Enter 1 or 2: ").strip()

    if choice not in {"1", "2"}:
        print("❌ Invalid choice. Exiting.")
        return

    email = input("📧 Email: ").strip()
    password = input("🔐 Password: ").strip()

    if choice == "2":
        await sign_up(email, password)
        print("📩 Please confirm your email before logging in.")
        return

    token = await login(email, password)
    if not token:
        print("🚫 Login failed. Cannot start chat.")
        return

    print("✅ Login successful!")
    await run_chat(token)


if __name__ == "__main__":
    asyncio.run(main())
