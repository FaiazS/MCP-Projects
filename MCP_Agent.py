import dotenv

from dotenv import load_dotenv

import asyncio

from agents import Agent, Runner, trace

from Playwright_MCP_Server import playwright_mcp_tool

from File_System_MCP_Server import file_system_tool

load_dotenv(override= True)

agent_instructions = """

Hey there, to describe yourself, here are your following characteristics:

   1. You are specialized at browsing the internet to accomplish your given tasks.

   2. While doing '1', you accept all cookies and click 'not now' as wherever appropriate to retrieve the content you require.

   3. You don't just stop at one website, but scan and analyze multiple websites and extract the most relevant, validated, verified and top notch quality content required for the given task at hand.  

   4. You are persistent in doing what you are specialized at till you have given the desired final output.

"""
async def web_research_agent():

 web_research_agent = Agent(

    name = 'Web browser Agent',

    instructions = agent_instructions,

    model = 'llama-3.3-70b-versatile',

    mcp_servers = [playwright_mcp_tool, file_system_tool]

 )

 with trace('Web Research Agent Task 1'):

    result = await Runner.run(starting_agent= web_research_agent, input= "Find a recipe for 'Coffee Bean and Tea Leaf' style Caramel Frappe with rich whipped cream and summarize and document it in markdown to caramel_frappe.md file")

    print(result.final_output)


if __name__ == '__main__':
  
   asyncio.run(web_research_agent())

