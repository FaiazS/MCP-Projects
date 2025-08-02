from equity_account_mcp_client import read_equity_report, get_all_equity_account_tools_openai_format, get_all_equity_account_tools

from equity_mcp_server_script_1 import agent_instructions, account_query, gpt

from agents import Agent, Runner, trace

from IPython.display import display, Markdown

from equity_account import EquityAccount

equity_mcp_tools = get_all_equity_account_tools()

print(equity_mcp_tools)

openai_formatted_tools = get_all_equity_account_tools_openai_format()

print(openai_formatted_tools)

async def run_mcp_client_script_1():

 with trace('equity_mcp_client_script_1'):

    equity_manager_agent = Agent(

        name = 'Equity portfolio manager',

        model = gpt,

        instructions = agent_instructions,

        tools = openai_formatted_tools

    )

    result = await Runner.run(equity_manager_agent, account_query)

    print(display(Markdown(result.final_output)))

    equity_account_context = await read_equity_report(name= 'Faiaz Ahmed')

    print(display(Markdown(equity_account_context)))

    print(EquityAccount.get_account_details('Faiaz Ahmed').equity_report())
