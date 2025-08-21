#!/usr/bin/python3
from typing import TypedDict,List
from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START,END
from dotenv import load_dotenv
import os

load_dotenv()  #load API keys

class AgentState(TypedDict):
    #tell the language model this is a human message
    messages:List[HumanMessage]

#set up our LLM in our casee llama on groq 
llm = ChatGroq(
    temperature=0.3,  # Lower temperature for more factual responses
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile"
)


#now create our nodes
def process(state: AgentState)->AgentState:
    response=llm.invoke(state["messages"])

    print(f"\nAI: {response.content}")
    return state

#create the graph
graph=StateGraph(AgentState)

#create the node
graph.add_node('process', process)

#set start and end
graph.add_edge(START, 'process')
graph.add_edge('process', END)

#compile the graph
agent=graph.compile()

while True:
    user_input=input("\nUSER: ")

    if user_input in ['exit', 'quit']:
        break
    #we invoke the agent by passing the human message to the agent
    agent.invoke({"messages":[HumanMessage(content=user_input)]})


"""
 python .\main.py

USER: hey

AI: Hello. How can I help you today?

USER: who are you

AI: I'm an artificial intelligence model known as Llama. Llama stands for "Large Languuage Model Meta AI."
"""