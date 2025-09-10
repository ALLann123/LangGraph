#!/usr/bin/python3
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
import asyncio


load_dotenv()

llm = ChatGroq(
    temperature=0,  # Lower temperature for more factual responses
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile"
)

model = llm

# connect to the MCP Server from firecrawl
server_params = StdioServerParameters(
    command="npx",
    env={
        'FIRECRAWL_API_KEY': os.getenv('FIRECRAWL_API_KEY'),
    },
    args=['firecrawl-mcp']
)

async def main():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await load_mcp_tools(session)

            agent = create_react_agent(
                model,
                tools
            )
            
            system_message = {
                "role": "system",
                "content": """You are a helpful assistant that can scrape websites, crawl pages, and extract data using Firecrawl tools.

                RULES:
                - For factual queries (best, top, reviews, destinations, etc.), you MUST use `firecrawl_search`.
                - firecrawl_search must only use {"query": "...", "sources": [{"type":"web"}]}.
                - Do not answer from memory. Always search first.
                """
            }

            print("Available Tools- ", *[tool.name for tool in tools])
            print("-" * 15)

            while True:
                user_input = input("\nYou: ")

                if user_input in ['exit', 'quit']:
                    break

                # Only send system + latest user input
                messages = [
                    system_message,
                    {"role": "user", "content": user_input[:175000]}
                ]

                try:
                    agent_response = await agent.ainvoke({"messages": messages})
                    ai_message = agent_response["messages"][-1].content
                    print("\nAgent:", ai_message)
                except Exception as e:
                    print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())



"""
 python .\main.py
Available Tools-  firecrawl_scrape firecrawl_map firecrawl_crawl firecrawl_check_crawl_status firecrawl_search firecrawl_extract
---------------

You: prices for visiting Maasai Mara, and diani bonfire adventures 

Agent: The current prices for visiting Maasai Mara and Diani Bonfire Adventures are as follows:

* 3 Days 2 Nights Safari Package: Ksh 14,000.00
* Park entry fees: USD 100 per day for non-residents
* 3 Nights Accommodation: included in the package
* Return Economy SGR Tickets: included in the package
* Return transfers in Mombasa: included in the package
* Travel insurance: included in the package

Please note that these prices are subject to change and may vary depending on the time of year and other factors. It's always best to check with Bonfire Adventures for the most up-to-date pricing and packages.
"""