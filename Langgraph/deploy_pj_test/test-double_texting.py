# main.py

import asyncio
import os
import httpx
from dotenv import load_dotenv
from langgraph_sdk import get_client

load_dotenv()

async def run_chat():
    """Run the chatbot after successful login."""
    client = get_client(
        url="http://localhost:8123",
    )

    thread = await client.threads.create()

  
    user_input_1 = "Tell me a song on love"
    user_input_2 = "Tell me a song on love"

    response_1 = await client.runs.wait(
        thread_id=thread["thread_id"],
        assistant_id="task_maistro",
        input={"messages": [{"role": "user", "content": user_input_1}]},
        config={"configurable": {"recursion_limit": 50}} 
    )

    response_2 = await client.runs.wait(
        thread_id=thread["thread_id"],
        assistant_id="task_maistro",
        input={"messages": [{"role": "user", "content": user_input_2}]},
        config={"configurable": {"recursion_limit": 50}} ,
    )
    reply_1 = response_1
    reply_2 = response_2
    print("Agent1:", reply_1, "\n")
    print("--------------------------------")
    print("Agent2:", reply_2, "\n")


async def main():
    await run_chat()


if __name__ == "__main__":
    asyncio.run(main())
