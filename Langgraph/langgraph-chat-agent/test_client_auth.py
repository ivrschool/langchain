import sys
import asyncio
from langgraph_sdk import get_client

async def test_auth(token: str | None):

    # Authenticated client
    client = get_client(
        url="http://localhost:2024",
        headers={"Authorization": f"Bearer {token}"}
    )

    try:
        thread = await client.threads.create()
        print("✅ Thread created successfully:", thread["thread_id"])
    except Exception as e:
        print("❌ Authentication failed:", e)
        return

    # Start chat loop
    print("Type 'exit' to quit the chat.")
    while True:
        user_input = input("You: ")
        if user_input.strip().lower() == "exit":
            break

        response = await client.runs.wait(
            thread_id=thread["thread_id"],
            assistant_id="agent",
            input={"messages": [{"role": "user", "content": user_input}]},
        )
        assistant_reply = response["messages"][-1]["content"]
        print("Agent:", assistant_reply, "\n")

if __name__ == "__main__":
    token = sys.argv[1] if len(sys.argv) > 1 else None
    asyncio.run(test_auth(token))
