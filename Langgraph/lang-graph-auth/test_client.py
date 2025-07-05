import asyncio
from langgraph_sdk import get_client

async def test_no_auth():
    client = get_client(url="http://localhost:2024")
    try:
        await client.threads.create()
        print("❌ Should have failed without token!")
    except Exception as e:
        print("✅ Blocked unauthenticated access:", e)

async def test_with_auth():
    client = get_client(
        url="http://localhost:2024",
        headers={"Authorization": "Bearer user1-token"}
    )
    thread = await client.threads.create()
    print(f"✅ Created thread as Alice: {thread['thread_id']}")
    # response = await client.runs.create(
    #     thread_id=thread["thread_id"],
    #     assistant_id="agent",
    #     input={"messages": [{"role": "user", "content": "Hi! I am Pankaj."}]}
    # )
    # print("✅ Bot responded:", "Success")

    response = await client.runs.wait(
    thread_id=thread["thread_id"],
    assistant_id="agent",
    input={"messages": [{"role": "user", "content": "how are you?"}]},
    )
    print(response["messages"][-1]["content"])
    
asyncio.run(test_no_auth())
print("--------------------------------")
asyncio.run(test_with_auth())
