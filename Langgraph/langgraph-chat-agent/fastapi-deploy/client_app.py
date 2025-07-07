# client_app.py

import asyncio
import os
import httpx
from getpass import getpass
from dotenv import load_dotenv
import uuid
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
API_URL = os.getenv("FASTAPI_URL", "http://localhost:8000")  # Your FastAPI server


async def sign_up(email: str, password: str):
    """Sign up a new user on Supabase."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{SUPABASE_URL}/auth/v1/signup",
            json={"email": email, "password": password},
            headers={"apikey": SUPABASE_ANON_KEY},
        )
        if response.status_code != 200:
            print("Signup failed:", response.text)
            return None
        print("Signup successful! Please confirm your email before logging in.")
        return response.json()


async def login(email: str, password: str) -> str | None:
    """Login and get JWT token."""
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
            print("Login failed:", response.text)
            return None
        return response.json()["access_token"]


async def run_chat(token: str,thread_id: str):
    """Chat with the FastAPI-secured LangGraph agent."""
    async with httpx.AsyncClient() as client:
        while True:
            user_input = input("You: ")
            if user_input.strip().lower() == "exit":
                break

            response = await client.post(
                f"{API_URL}/chat",
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                },
                json={"message": user_input, "thread_id":thread_id}
            )
            if response.status_code != 200:
                print("Error:", response.text)
                continue

            reply = response.json()["content"]
            print("Agent:", reply, "\n")


async def main():
    print("Welcome! Do you want to:")
    print("1. Login")
    print("2. Sign up")

    choice = input("Enter 1 or 2: ").strip()

    if choice not in {"1", "2"}:
        print("Invalid choice. Exiting.")
        return

    email = input("Email: ").strip()
    password = getpass("Password: ").strip()

    if choice == "2":
        await sign_up(email, password)
        return

    token = await login(email, password)
    if not token:
        print("Login failed. Cannot start chat.")
        return

    print("Login successful. Type 'exit' to quit.")
    thread_id = str(uuid.uuid4())
    await run_chat(token,thread_id)


if __name__ == "__main__":
    asyncio.run(main())
