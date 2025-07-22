import os

import dotenv

from agents import Agent, Runner, trace, gen_trace_id

from agents.mcp import MCPServerStdio

import asyncio

from dotenv import load_dotenv

async def file_system_tool():

    file_system_tool_path = os.path.abspath(os.path.join(os.getcwd(), 'file_system_tool_path'))

    file_system_tool_parameters = {'command': 'npx', 'args': ['-y', '@modelcontextprotocol/server-filesystem', file_system_tool_path]}

    async with MCPServerStdio(params = file_system_tool_parameters, client_session_timeout_seconds = 30) as file_system_mcp_server:

        file_tools = await file_system_mcp_server.list_tools()

        tool_list = [{'File tool name': tool.name, 'File tool purpose' : tool.description} for tool in file_tools]

        print(f"Available file tools and usage: {tool_list}")

if __name__ == '__main__':

    asyncio.run(file_system_tool())
