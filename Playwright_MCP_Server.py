import dotenv

from dotenv import load_dotenv

from agents import Agent, Runner, trace, gen_trace_id

from agents.mcp import MCPServerStdio

import asyncio

load_dotenv(override = True)

async def playwright_mcp_tool():

    playwright_parameters = {'command': 'npx', 'args': ['@playwright/mcp@latest']}

    async with MCPServerStdio(params = playwright_parameters, client_session_timeout_seconds = 30) as playwright_mcp_server:

        playwright_tools = await playwright_mcp_server.list_tools()

        tool_list = [{'Tool name' : tool.name, 'Tool purpose': tool.description} for tool in playwright_tools]

        print(f"Tools available : {tool_list}")

if __name__ == '__main__':

    asyncio.run(playwright_mcp_tool())
