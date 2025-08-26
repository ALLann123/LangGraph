#!/usr/bin/python3
import os
from dotenv import load_dotenv
from typing import Annotated, Literal
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field
from typing_extensions import TypedDict

load_dotenv()

#set up our LLM in our casee llama on groq 
llm = ChatGroq(
    temperature=0.3,  # Lower temperature for more factual responses
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile"
)

#state graph schema- COntrol the flow of our application
class State(TypedDict):
    #store new messages from the user and the LLM. Annotated we take two inputs.add_messages appends to our state new message
    messages: Annotated[list,add_messages]

#make node- Take in the current state then return the modification of our graph
def chatbot(state:State)->State:
    #we take in the updated state and pass it to the llm and return is
    return {"messages":[llm.invoke(state["messages"])]}


#Make the graph
graph_builder=StateGraph(State)

#add a node
graph_builder.add_node('chatbot',chatbot)

#connect to the start
graph_builder.add_edge(START, 'chatbot')

#connect to the end
graph_builder.add_edge('chatbot', END)

#compile the graph
graph=graph_builder.compile()


user_input=input("Enter a message: ")

#when we invoke the graph we pass in the state we want the graph to start with
state=graph.invoke({'messages':[{'role':'user','content':user_input}]})
print(state['messages'][-1].content)



"""
python .\main.py
Enter a message: What is the square root of 49
The square root of 49 is 7.
"""