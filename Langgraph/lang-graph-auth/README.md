# LangGraph Chat Interface

This directory contains a simple chat interface for interacting with LangGraph agents.

## Files

- `chat_loop.py` - Main chat loop implementation
- `run_chat.py` - Simple script to run the chat loop
- `test_client.py` - Basic test client for authentication

## Usage

### Prerequisites

1. Make sure your LangGraph server is running on `http://localhost:2024`
2. Ensure you have the required authentication token (`user1-token`)

### Running the Chat Loop

You can run the chat interface in two ways:

#### Method 1: Direct Python execution
```bash
python chat_loop.py
```

#### Method 2: Using the run script
```bash
python run_chat.py
```

### Features

- **Interactive Chat**: Type messages and get AI responses in real-time
- **Session Management**: Creates a new thread for each chat session
- **Error Handling**: Graceful handling of connection issues and parsing errors
- **Exit Commands**: Type `quit`, `exit`, or `bye` to end the conversation
- **Keyboard Interrupt**: Press `Ctrl+C` to interrupt and exit

### Example Session

```
🚀 Starting LangGraph Chat Interface
==================================================
🤖 Chat session started! Thread ID: abc123-def456
💬 Type 'quit' or 'exit' to end the conversation
--------------------------------------------------

👤 You: Hello, how are you?
🤔 AI is thinking...

🤖 AI: Hello! I'm doing well, thank you for asking. How can I help you today?

👤 You: What's the weather like?
🤔 AI is thinking...

🤖 AI: I don't have access to real-time weather information, but I'd be happy to help you with other questions or tasks!

👤 You: quit

👋 Goodbye! Ending chat session...
```

### Troubleshooting

- **Connection Error**: Make sure your LangGraph server is running
- **Authentication Error**: Verify your authentication token is correct
- **Response Parsing Error**: The chat loop will show the response structure for debugging

## Customization

You can modify the chat loop by editing `chat_loop.py`:

- Change the server URL in the `get_client()` call
- Modify the authentication headers
- Adjust the message parsing logic
- Add custom commands or features
