import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from agent import create_react_agent  
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# List of tool names that should always be used (the agent must not calculate itself)
TOOL_ONLY_TASKS = {"multiply_numbers", "subtract_numbers"}

async def main():
    server_params = StdioServerParameters(
        command="python",
        args=["mcp_server.py"], 
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            all_tools = await load_mcp_tools(session)

            # Filter tools that must be tool-invoked only
            strict_tools = [tool for tool in all_tools if tool.name in TOOL_ONLY_TASKS]

            # Optional: include all tools in agent, or only the strict ones
            agent = create_react_agent(model, strict_tools)

            # Create system prompt only for specific tools
            if strict_tools:
                tool_descriptions = "\n".join(
                    f"- {tool.name}: {tool.description}" for tool in strict_tools
                )

                system_instruction = (
                    "You are a smart assistant. For general conversation and reasoning, you may use your own thinking.\n"
                    "However, for the following operations, you must never calculate by yourself. "
                    "Always use the tools listed below:\n\n"
                    f"{tool_descriptions}\n\n"
                    "if user asks something that requries other tool, use your own thinking and answer it."
                    
                )
                system_message = SystemMessage(content=system_instruction)
            else:
                system_message = SystemMessage(content="You are a helpful assistant. Use your own reasoning freely.")

            print("Calculator Assistant is ready. Type 'exit' to quit.\n")

            while True:
                user_input = input("You: ").strip()
                if user_input.lower() in {"exit", "quit"}:
                    print("Exiting...")
                    break

                input_messages = [system_message, HumanMessage(content=user_input)]

                try:
                    result = await agent.ainvoke({"messages": input_messages})
                    for m in result["messages"]:
                        m.pretty_print()
                except Exception as e:
                    print("Error:", e)

if __name__ == "__main__":
    asyncio.run(main())
