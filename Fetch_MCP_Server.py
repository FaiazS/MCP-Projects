import dotenv

from dotenv import load_dotenv

from agents import Agent, Runner, trace, gen_trace_id

from agents.mcp import MCPServerStdio

import asyncio

load_dotenv(override=True)

async def fetch_mcp_server():

 fetch_parameters = {'command': 'uvx', 'args': ['mcp-server-fetch']}

 async with MCPServerStdio(params = fetch_parameters, client_session_timeout_seconds = 60) as fetch_mcp_server:

    fetch_tools = await fetch_mcp_server.list_tools()

    tool_list = [{'Tool name' : tool.name, 'Tool purpose' : tool.description} for tool in fetch_tools]

    print(f"Tools available: {tool_list}")

if __name__ == '__main__':
  
   asyncio.run(fetch_mcp_server())
