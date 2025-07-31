import mcp

import json

from agents import FunctionTool

from mcp import StdioServerParameters

from mcp.client.stdio import stdio_client

equity_account_mcp_server_parameters = StdioServerParameters(command = 'uv', args = ['run', 'equity_account_mcp_server.py'], env = None)

async def get_all_equity_account_tools():

    async with stdio_client(server=equity_account_mcp_server_parameters) as client_stream:

        async with mcp.ClientSession(*client_stream) as client_session:

            await client_session.initialize()

            equity_account_tools = await client_session.list_tools()

            return equity_account_tools.tools


async def call_equity_account_tool(tool_name, tool_args):

    async with stdio_client(server=equity_account_mcp_server_parameters) as client_stream:

        async with mcp.ClientSession(*client_stream) as client_session:

            await client_session.initialize()

            tool = await client_session.call_tool(tool_name, tool_args)

            return tool
        

async def read_equity_report(name):

    async with stdio_client(server=equity_account_mcp_server_parameters) as client_stream:

        async with mcp.ClientSession(*client_stream) as client_session:

            await client_session.initialize()

            equity_report = await client_session.read_resource(f'equity_account://equity_report/{name}')

            return equity_report.contents[0].text


async def read_equity_investment_strategy(name):

    async with stdio_client(server=equity_account_mcp_server_parameters) as client_stream:

        async with mcp.ClientSession(*client_stream) as client_session:

            await client_session.initialize()

            equity_investment_strategy = await client_session.read_resource(f'equity_account://equity_investment_strategy/{name}')

            return equity_investment_strategy.contents[0].text


async def get_all_equity_account_tools_openai_format():

    openai_formatted_tools = []

    for tool in await get_all_equity_account_tools():

        openai_tools_schema = {**tool.inputSchema, 'additionalProperties' : False}

        openai_format_tools = FunctionTool(
            
                                           name = tool.name, 
                                           
                                           description = tool.description, 
                                           
                                           params_json_schema = openai_tools_schema,

                                           on_invoke_tool = lambda ctx, 
                                           
                                                                   args, 
                                                                   
                                                                   toolname = tool.name: call_equity_account_tool(tool_name=toolname, tool_args=json.loads(args))
                                           
                                           )
        
        openai_formatted_tools.append(openai_format_tools)

        return openai_formatted_tools
