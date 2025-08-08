import os

import asyncio

from dotenv import load_dotenv

from agents import add_trace_processor

from equity_market import is_equity_market_open

from typing import List

from agent_tracers import AgentLogTracer

from trader_agents import TraderAgent

load_dotenv(override=True)

RUN_EVERY_N_MINUTES = int(os.getenv('RUN_EVERY_N_MINUTES'))

RUN_EVEN_WHEN_MARKET_IS_CLOSED = os.getenv('RUN_EVEN_WHEN_MARKET_IS_CLOSED')

USE_MANY_MODELS = os.getenv('USE_MANY_MODELS')

trader_agents_firstnames = ['Warren', 'George', 'Ray', 'Cathie']

trader_agents_lastnames = ['Dave',  'Liamson', 'Brooke', 'Rowling']

if USE_MANY_MODELS:

    model_names = ['openai/gpt-oss-20b', 'llama-3.3-70b-versatile', 'qwen/qwen3-coder', 'gemini-2.0-flash']

    short_model_names = ['gpt-oss-20b', 'llama-3.3-70b-versatile', 'qwen3-coder', 'gemini-2.0-flash']

else:

    model_names = ['gpt-4o'] * 4

    short_model_names = ['gpt-40'] * 4


def register_trader_agents() -> List[TraderAgent]:

    trader_agents = []

    for firstname, lastname, model_name in zip(trader_agents_firstnames, trader_agents_lastnames):

        trader_agents.append(TraderAgent(name = firstname, lastname = lastname, model_name = model_name))

    return trader_agents

async def trade_every_n_minutes():

    add_trace_processor(AgentLogTracer())

    trader_agents = register_trader_agents()

    if is_equity_market_open() or RUN_EVEN_WHEN_MARKET_IS_CLOSED:

        await asyncio.gather(*[trader_agent.initialize_trading_session() for trader_agent in trader_agents])

    else:

        print('Equity Market Closed!.')

    await asyncio.sleep(RUN_EVEN_WHEN_MARKET_IS_CLOSED * 60)


if __name__ == '__main__':

    print(f'Initializing trade session for every {RUN_EVEN_WHEN_MARKET_IS_CLOSED} minutes.')

    asyncio.run(trade_every_n_minutes())