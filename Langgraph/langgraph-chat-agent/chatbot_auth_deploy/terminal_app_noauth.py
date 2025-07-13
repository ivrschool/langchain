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
        url="http://localhost:2024",
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
            config={"configurable": {"recursion_limit": 50}} 
        )
        reply = response["messages"][-1]["content"]
        print("Agent:", reply, "\n")


async def main():
    await run_chat()


if __name__ == "__main__":
    asyncio.run(main())
