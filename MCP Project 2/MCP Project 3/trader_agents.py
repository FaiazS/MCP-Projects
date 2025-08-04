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


async def financial_researcher_tools(model, mcp_server) -> Tool:

    financial_researcher = await financial_researcher_agent(model = model, mcp_server = mcp_server)

    return financial_researcher.as_tool(tool_name = 'Financial research tool', tool_description = financial_research_tool())













