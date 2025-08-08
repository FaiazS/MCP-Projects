import os

import json

from dotenv import load_dotenv

from agents.mcp import MCPServerStdio

from openai import AsyncOpenAI

from agent_instructions import (
                               
                               financial_researcher_instructions, 

                               financial_research_tool, 

                               investor_trader_instructions, 
                               
                               trade_invest_message, 

                               rebalance_equity_portfolio_message
                               
                               )

from mcp_server_configurations import trader_mcp_server, researcher_mcp_server

from contextlib import AsyncExitStack

from equity_account_mcp_client import read_equity_report, read_equity_investment_strategy

from agents import trace, Agent, Runner, Tool, OpenAIChatCompletionsModel

from agent_tracers import generate_agent_trace_id

load_dotenv(override=True)

MAX_ROUNDS = 30

groq_api_key = os.getenv('GROQ_API_KEY')

google_gemini_api_key = os.getenv('GOOGLE_GEMINI_API_KEY')

open_router_api_key= os.getenv('OPENROUTER_API_KEY')

GROQ_BASE_URL = 'https://api.groq.com/openai/v1'

GOOGLE_GEMINI_BASE_URL = 'https://generativelanguage.googleapis.com'

OPENROUTER_BASE_URL = 'https://openrouter.ai/api/v1'

groq_client = AsyncOpenAI(base_url= GROQ_BASE_URL, api_key = groq_api_key)

google_gemini_client = AsyncOpenAI(base_url = GOOGLE_GEMINI_BASE_URL, api_key = google_gemini_api_key)

openrouter_client = AsyncOpenAI(base_url = OPENROUTER_BASE_URL, api_key = open_router_api_key)

def get_ai_model(ai_model: str):

    if '/' in ai_model:

        return OpenAIChatCompletionsModel(model = ai_model, openai_client= openrouter_client)
    
    elif 'groq' in ai_model:

        return OpenAIChatCompletionsModel(model = ai_model, openai_client = groq_client)
    
    elif 'gemini' in ai_model:

        return OpenAIChatCompletionsModel(model = ai_model, openai_client= google_gemini_client)
    
    else:

        return ai_model
    

async def financial_researcher_agent(model, mcp_server) -> Agent:

    researcher_agent = Agent(

        name = 'Financial Research Agent',

        model = model,

        instructions = financial_researcher_instructions(),

        mcp_servers = [mcp_server]

    )
    return researcher_agent

async def financial_researcher_tools(model, mcp_server) -> Tool:

    financial_researcher = await financial_researcher_agent(model = model, mcp_server = mcp_server)

    return financial_researcher.as_tool(tool_name = 'Financial research tool', tool_description = financial_research_tool())

class TraderAgent:

    def __init__(self, name: str, lastname = 'Agent', model_name = 'gpt-4o'):

        self.name = name

        self.lastname = lastname

        self.agent = None

        self.model_name = model_name

        self.do_trade = True

    async def define_agent(self, trader_agent_mcp_server, researcher_agent_mcp_server) -> Agent:

        agent_tools = await financial_researcher_tools(self.model_name, researcher_agent_mcp_server)

        self.agent = Agent(

            name = self.name,

            model = get_ai_model(self.model_name),

            instructions = investor_trader_instructions(name = self.name),

            tools = [agent_tools],

            mcp_servers = trader_agent_mcp_server
        )

    async def get_equity_account_report(self) -> str:

        equity_account_report = await read_equity_report(name = self.name)

        equity_account_report_json =  json.loads(equity_account_report)

        equity_account_report_json.pop('account_portfolio_value_time_series', None)

        return json.dumps(equity_account_report_json)
    

    async def initialize_agent_trade(self, trader_agent_mcp_server, researcher_agent_mcp_server):

        self.agent = await self.define_agent(trader_agent_mcp_server= trader_agent_mcp_server, researcher_agent_mcp_server= researcher_agent_mcp_server)

        equity_account = await self.get_equity_account_report()

        investment_strategy = await read_equity_investment_strategy(name = self.name)

        agent_trade_message = (trade_invest_message(name = self.name, investment_strategy = investment_strategy, account_name = equity_account) if self.do_trade else rebalance_equity_portfolio_message(name = self.name, investment_strategy = investment_strategy, account_name = equity_account))

        await Runner.run(self.agent, agent_trade_message, max_turns= MAX_ROUNDS)

    
    async def initialize_mcp_servers(self):

        async with AsyncExitStack() as mcp_stack:

            trader_agent_mcp_server = [await mcp_stack.enter_async_context(

                MCPServerStdio(params = mcp_server_parameters, client_session_timeout_seconds = 120) for mcp_server_parameters in trader_mcp_server

            )]

            researcher_agent_mcp_server = [await mcp_stack.enter_async_context(

                MCPServerStdio(params = mcp_server_parameters, client_session_timeout_seconds = 120) for mcp_server_parameters in researcher_mcp_server

            )]
            
            await self.initialize_agent_trade(trader_agent_mcp_server = trader_agent_mcp_server, researcher_agent_mcp_server = researcher_agent_mcp_server)


    async def initialize_agent_trace(self):

        agent_trace_name = f'Trading - {self.name}' if self.do_trade else f'Rebalancing portfolio{self.name}'

        agent_trace_id = generate_agent_trace_id(agent_tag = agent_trace_name)

        with trace(agent_trace_name, trace_id = agent_trace_id):

             await self.initialize_mcp_servers()


    async def initialize_trading_session(self):

        try: 

            await self.initialize_agent_trace()

        except Exception as e:

            print(f'Error running trading agent {self.name}: {e}')

        self.do_trade = not self.do_trade