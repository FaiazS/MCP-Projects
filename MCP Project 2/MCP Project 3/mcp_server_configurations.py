import os

from dotenv import load_dotenv

load_dotenv(override=True)

brave_search_env = {'BRAVE_API_KEY': os.getenv('BRAVE_API_KEY')}

account_name = 'Faiaz Ahmed'

def trader_mcp_server_parameters():

 equity_account_mcp_server_parameters = {'command': 'uv', 'args': ['run', 'equity_account_mcp_server.py']}

 equity_market_mcp_server_parameters = {'command': 'uv', 'args': ['run', 'equity_market_mcp_server.py']}

 push_notification_mcp_server_parameters = {'command': 'uv', 'args': ['run', 'pushover_mcp_server.py']}

 trader_mcp_server_parameters = [equity_account_mcp_server_parameters, push_notification_mcp_server_parameters, equity_market_mcp_server_parameters]

 return trader_mcp_server_parameters

def researcher_mcp_server_parameters(name: str):
 
 fetch_mcp_server_parameters = {'command': 'uv', 'args': ['fetch-mcp-server']}

 brave_mcp_server_parameters = {'command': 'npx', 'args': ['-y','@modelcontextprotocol/server-brave-search'], 'env': brave_search_env}

 libsql_mcp_server_parameters = {'command': 'npx', 'args': ['-y', 'mcp-memory-libsql'], 'env': f'file:./agent_memory/{name}.db'}

 researcher_mcp_server_parameters_list = [fetch_mcp_server_parameters, brave_mcp_server_parameters, libsql_mcp_server_parameters]

 return researcher_mcp_server_parameters_list

trader_mcp_server = trader_mcp_server_parameters()

researcher_mcp_server = researcher_mcp_server_parameters(name= account_name)