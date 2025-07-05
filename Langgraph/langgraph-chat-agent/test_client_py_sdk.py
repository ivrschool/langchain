from langgraph_sdk import get_client
import asyncio

async def run_test():
    client = get_client(url="http://localhost:2024")
    thread = await client.threads.create()

    while True:
        user_input = input("You: ")
        if user_input.strip().lower() == "exit":
            break

        response = await client.runs.wait(
                        thread_id=thread["thread_id"],
                        assistant_id="agent",
                        input={"messages": [{"role": "user", "content": user_input}]},
                        config={"configurable": {"recursion_limit": 50 }}
                        )
        assistant_reply = response["messages"][-1]["content"]
        print("Agent:", assistant_reply, "\n")


asyncio.run(run_test())


