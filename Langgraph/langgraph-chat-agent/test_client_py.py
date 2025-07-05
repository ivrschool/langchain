import http.client
import json
import uuid
import time

HOST = "127.0.0.1"
PORT = 2024
GRAPH_ID = "agent"

def create_assistant():
    conn = http.client.HTTPConnection(HOST, PORT)
    assistant_id = str(uuid.uuid4())

    payload = json.dumps({
        "assistant_id": assistant_id,
        "graph_id": GRAPH_ID,
        "config": {},
        "metadata": {},
        "if_exists": "raise",
        "name": "cli_assistant",
        "description": "Assistant created via HTTP API"
    })

    headers = {'Content-Type': 'application/json'}
    conn.request("POST", "/assistants", payload, headers)

    response = conn.getresponse()
    data = json.loads(response.read().decode("utf-8"))

    return data.get("assistant_id", assistant_id)

def create_thread():
    conn = http.client.HTTPConnection(HOST, PORT)
    thread_id = str(uuid.uuid4())

    payload = json.dumps({
        "assistant_id": None,
        "thread_id": thread_id,
        "graph_id": GRAPH_ID,
        "config": {},
        "metadata": {},
        "name": "cli_chat_thread"
    })

    headers = {'Content-Type': 'application/json'}
    conn.request("POST", "/threads", payload, headers)

    response = conn.getresponse()
    data = json.loads(response.read().decode("utf-8"))

    return data.get("thread_id", thread_id)

def create_run_and_wait(thread_id, assistant_id, message):
    conn = http.client.HTTPConnection(HOST, PORT)

    payload = json.dumps({
        "thread_id": thread_id,
        "assistant_id": assistant_id,
        "input": {
            "messages": [{"role": "user", "content": message}]
        },
        "command": None,
        "metadata": {},
        "config": {
            "recursion_limit": 50,
            "configurable": {}
        },
        "stream_mode": ["values"],
        "checkpoint_during": False,
        "on_completion": "keep"
    })

    headers = {'Content-Type': 'application/json'}
    conn.request("POST", "/runs/wait", payload, headers)

    response = conn.getresponse()
    data = json.loads(response.read().decode("utf-8"))

    return data.get("messages")[-1]["content"]

def main():
    print("Starting LangGraph HTTP chat loop...")
    assistant_id = create_assistant()
    thread_id = create_thread()

    print("Chat started. Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")
        if user_input.strip().lower() == "exit":
            break
        reply = create_run_and_wait(thread_id, assistant_id, user_input)
        print("Agent:", reply)
        print()

if __name__ == "__main__":
    main()
