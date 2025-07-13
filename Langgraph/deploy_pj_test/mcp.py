# from langchain_mcp_adapters.client import MultiServerMCPClient


# from langchain_mcp_adapters.client import Connection

# async def get_mcp_tools_node():
    

#     async def _get_tools():
#         client = MultiServerMCPClient({
#             "agent": Connection(
#                 transport="streamable_http",
#                 url="http://localhost:8123/mcp"
#             )
#         })
#         tools = await client.get_tools()
#         return {"tools": tools}

#     return asyncio.run(_get_tools())

# if __name__ == "__main__":
#     asyncio.run(get_mcp_tools_node())   