import os

import asyncio

from dotenv import load_dotenv

from agents import Agent, Runner, trace

from agents.mcp import MCPServerStdio

from IPython.display import display, Markdown

from datetime import datetime

load_dotenv(override=True)

agent_memory_parameters = {'command': 'npx', 'args': ['-y', 'mcp-memory-libsql'], 'env': {'LIBSQL_URL' : 'file:./agent_memory/agent_memory.db'}}

async def initialize_agent_memory():

    async with MCPServerStdio(params= agent_memory_parameters, client_session_timeout_seconds = 30) as agent_memory_server:

      agent_memory_tools = await agent_memory_server.list_tools()

      tool_list = [(f'Tool name: {tool.name}', f'Tool purpose: {tool.description}') for tool in agent_memory_tools]

      print(tool_list)

async def initialize_memory_agent():
   
   agent_instruction = """
   
                          You are an agent who leverages: 
   
                            1. Tools as a persistent memory to store and recall context of your prior conversations.
                          
                          """

   user_input = """

                    My name is Faiaz, and I am an aspiring AI and Software Engineer.

                    I have taken the course on Agentic AI, which covers the recent and widely adopted MCP Protocol.

                    MCP refers to a protocol which which eases the integration of tools, resources and prompt templates into LLM-based agents, thus providing them capabilities according to the task at hand to not just generate text, but reason, plan, and act autonomously and deliver quality output with minimal human intervention.

                  """
   

   follow_up_user_input = "My name is Faiaz, what do you know about me?"


   gpt = 'gpt-4o'

   async with MCPServerStdio(params = agent_memory_parameters, client_session_timeout_second =  30) as agent_memory_server:
      
      agent = Agent(
         
                    name = 'Agent with Memory',
                    
                    model = gpt,
                    
                    instructions = agent_instruction,

                    mcp_servers = [initialize_agent_memory()]

                    )

      with trace('Agent with Memory'):

        result = await Runner.run(agent, user_input)
        
        print(display(Markdown(result.final_output)))


   async with MCPServerStdio(params=agent_memory_parameters, client_session_timeout_seconds= 30) as agent_memory_server:
      
      agent = Agent(
         
         name = 'Agent with Memory',

         instructions =  agent_instruction,

         model = gpt,

         mcp_servers = [initialize_agent_memory()]

      )

      with trace('Agent with Memory'):
         
        follow_up_result = await Runner.run(agent, follow_up_user_input)
        
        print(display(Markdown(follow_up_result.final_output)))

if __name__ == '__main__':

    asyncio.run(initialize_memory_agent())