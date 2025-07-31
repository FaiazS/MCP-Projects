import asyncio

from agents import Agent, Runner, trace

from agents.mcp import MCPServerStdio

from IPython.display import display, Markdown

from dotenv import load_dotenv

from equity_account import EquityAccount

load_dotenv(override=True)

equity_mcp_server_parameters = {'command': 'uv', 'args': ['run', 'equity_account_mcp_server.py']}

async def initialize_equity_mcp_server():

  async with MCPServerStdio(params= equity_mcp_server_parameters, client_session_timeout_seconds= 30) as equtiy_account_server:

    equity_account_tools = equtiy_account_server.list_tools()

    tool_list = [tool.name for tool in equity_account_tools]

    print(f"Available tools: {tool_list}")

agent_instructions = """You are a exceptional equity account manager who seamlessly manage equity portfolios for multiple clients.

                       You are specialized in:

                       1. Addressing queries regarding equity portfolios.

"""

account_query = "My name is Faiaz Ahmed and my equity portfolio is under the name 'Faiaz Ahmed', can you please lookup my current balance and equity holdings and update me on the same?"

gpt = 'gpt-4o'

async def initialize_account_manager_agent():
  
  async with MCPServerStdio(params = equity_mcp_server_parameters, client_session_timeout_seconds= 30) as equity_account_server_2:

    equity_manager_agent = Agent(
      
          name='Equity portfolio manager', 
          
          model= gpt, 
          
          instructions= agent_instructions, 
          
          mcp_servers = [initialize_equity_mcp_server()]
          
          )
    
    with trace('equity_account_manager'):
      
      result = await Runner.run(equity_manager_agent, account_query)

      print(display(Markdown(result.final_output)))


if __name__ == '__main__':
  
  asyncio.run(initialize_account_manager_agent())


