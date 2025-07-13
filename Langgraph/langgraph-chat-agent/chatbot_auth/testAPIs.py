import asyncio
import os
import httpx
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import httpx
from uuid import uuid4
# from main import login  # Reuse your login function

load_dotenv()


SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_ANON_KEY = os.environ["SUPABASE_ANON_KEY"]
LOGIN_EMAIL = os.environ["CRON_USER_EMAIL"]
LOGIN_PASSWORD = os.environ["CRON_USER_PASSWORD"]

BASE_URL = "http://localhost:2024"



HEADERS = {}

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

def success(name):
    print(f"✅ {name} succeeded")


def failure(name, response):
    print(f"❌ {name} failed: {response.status_code} - {response.text}")


async def create_assistant():
    assistant_id = str(uuid4())
    payload = {
        "assistant_id": assistant_id,
        "graph_id": "agent",
        "config": {}
    }
    async with httpx.AsyncClient() as client:
        res = await client.post(f"{BASE_URL}/assistants", headers=HEADERS, json=payload)
        if res.status_code == 200:
            success("Create Assistant")
            return res.json()["assistant_id"]
        else:
            failure("Create Assistant", res)
            return None


async def create_thread():
    payload = {}
    async with httpx.AsyncClient() as client:
        res = await client.post(f"{BASE_URL}/threads", headers=HEADERS, json=payload)
        if res.status_code == 200:
            success("Create Thread")
            return res.json()["thread_id"]
        else:
            failure("Create Thread", res)
            return None


async def create_cron(assistant_id, thread_id):
    end_time = (datetime.utcnow() + timedelta(days=1)).isoformat() + "Z"
    payload = {
        "schedule": "* * * * *",  # every minute
        "assistant_id": assistant_id,
        "end_time": end_time
    }
    async with httpx.AsyncClient() as client:
        res = await client.post(f"{BASE_URL}/threads/{thread_id}/cron", headers=HEADERS, json=payload)
        if res.status_code == 200:
            success("Create Cron")
            return res.json()["cron_id"]
        else:
            failure("Create Cron", res)
            return None


async def search_crons(assistant_id, thread_id):
    payload = {
        "assistant_id": assistant_id,
        "thread_id": thread_id,
        "limit": 5,
        "offset": 0
    }
    async with httpx.AsyncClient() as client:
        res = await client.post(f"{BASE_URL}/crons/search", headers=HEADERS, json=payload)
        if res.status_code == 200:
            success("Search Crons")
        else:
            failure("Search Crons", res)


async def delete_cron(cron_id):
    async with httpx.AsyncClient() as client:
        res = await client.delete(f"{BASE_URL}/crons/{cron_id}", headers=HEADERS)
        if res.status_code == 200:
            success("Delete Cron")
        else:
            failure("Delete Cron", res)


async def main():
    global HEADERS
    token = await login(LOGIN_EMAIL, LOGIN_PASSWORD)
    if not token:
        print("🚫 Login failed.")
        return

    HEADERS = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    assistant_id = await create_assistant()
    if not assistant_id:
        return

    thread_id = await create_thread()
    if not thread_id:
        return

    cron_id = await create_cron(assistant_id, thread_id)
    if not cron_id:
        return

    await search_crons(assistant_id, thread_id)
    await delete_cron(cron_id)


if __name__ == "__main__":
    asyncio.run(main())


