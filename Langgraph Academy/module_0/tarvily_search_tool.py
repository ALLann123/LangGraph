#!/usr/bin/python3
from dotenv import load_dotenv
from langchain_community.tools.tavily_search import  TavilySearchResults
import os

#load environment variables
load_dotenv()

#lets create the search tool and add our API key
tavily_search=TavilySearchResults(max_results=2, tavily_api_key=os.getenv("TAVILY_API_KEY"))

#lets now run our searches
search_docs=tavily_search.invoke("where did ruto travel to recently?")

print(search_docs)


