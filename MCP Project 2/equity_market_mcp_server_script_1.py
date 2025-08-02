import os

import asyncio

import equity_market

from agents.mcp import MCPServerStdio

from agents import Agent, Runner, trace

from IPython.display import display, Markdown

from dotenv import load_dotenv

equity_market_parameters = {'command': 'uv', 'args': ['run','equity_market_mcp_server.py']}

load_dotenv(override=True)

gpt = 'gpt-4o'

async def initialize_equity_market_mcp_server():

    async with MCPServerStdio(params = equity_market_parameters, client_session_timeout_seconds = 30) as equity_market_server:

        equity_market_tools = await equity_market_server.list_tools()

        tools_list = [(f'Tool name: {tool.name}, Tool description: {tool.description}') for tool in equity_market_tools]

        print(tools_list)

    agent_instruction =  "You are an extremely reliable assistant who help clarifies up to date news regarding the equity market."

    user_input = "Get me the most recent equity price of Amazon."

    with trace('Agent Conversation'):

        equity_market_agent = Agent(

            name = 'Agent',

            model = gpt,

            instructions= agent_instruction,

            mcp_servers = [equity_market_server]

        ) 

        equity_price = await Runner.run(equity_market_agent, user_input)

        print(display(Markdown(equity_price.final_output)))


if __name__ == '__main__':

    asyncio.run(initialize_equity_market_mcp_server())
