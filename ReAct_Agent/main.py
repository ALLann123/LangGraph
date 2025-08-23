#!/usr/bin/python3
from typing import Annotated, Sequence, TypedDict
from dotenv import load_dotenv
import os
from langchain_core.messages import BaseMessage
from langchain_core.messages import ToolMessage
from langchain_core.messages import SystemMessage
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from langgraph.graph import add_messages
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

load_dotenv()

#set up our LLM in our casee llama on groq 
llm = ChatGroq(
    temperature=0.3,  # Lower temperature for more factual responses
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile"
)


#create the state schema
class AgentState(TypedDict):
    #REDUCER function: reserve the state by appending and not overriding
    messages: Annotated[Sequence[BaseMessage],add_messages]


#we use a tool decorator to create a tool
@tool
def add(a:int, b:int)->int:
    """This is an addition function that adds 2 numbers together"""
    return a+b

@tool
def subtract(a: int, b:int)->int:
    """Use this to perform subtraction"""
    return a-b

@tool
def multiply(a: int, b: int):
    """Multiplication function"""
    return a*b

#now add the tool for our model
tools=[add, subtract,multiply]
model=llm.bind_tools(tools)

#add node
def model_call(state: AgentState)->AgentState:
    system_prompt=SystemMessage(content=
        "You are my AI Assistant, please Answer my query to the best of your ability."                            
    )
    #pass our system prompt
    response=model.invoke([system_prompt] + state["messages"])
    #now update the graph state
    return {"messages": [response]}

#this is a conditional edge node
def should_continue(state:AgentState):
    messages=state['messages']
    last_message=messages[-1]
    if not last_message.tool_calls:
        return "end"
    else: 
        return "continue"
    

#build the graph
graph=StateGraph(AgentState)

#add node
graph.add_node('our_agent', model_call)

#now add the tool node to our graph
tool_node=ToolNode(tools=tools)
graph.add_node("tools", tool_node)

#add edges to connect the node
graph.set_entry_point("our_agent")

#this connects our agent to the tools. Conditionally
graph.add_conditional_edges(
    "our_agent", #source node
    should_continue, #action
    {
        "continue":"tools",
        "end":END 
    }
)

#add the edge to connect the tool node to our agent
graph.add_edge("tools", "our_agent")

#comile graph
app=graph.compile()

def print_stream(stream):
    for s in stream:
        message=s["messages"][-1]

        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()

inputs={"messages":[("user", "Add 40 plus 12, subtract 5 and multiply the results by 6")]}
print_stream(app.stream(inputs, stream_mode="values"))

"""
python .\main.py
================================ Human Message =================================

Add 40 plus 12, subtract 5 and multiply the results by 6
================================== Ai Message ==================================
Tool Calls:
  add (a7fnmw33a)
 Call ID: a7fnmw33a
  Args:
    a: 40
    b: 12
  subtract (5qfs028we)
 Call ID: 5qfs028we
  Args:
    a: 52
    b: 5
  multiply (wm2ycm6a7)
 Call ID: wm2ycm6a7
  Args:
    a: 47
    b: 6
================================= Tool Message =================================
Name: multiply

282
================================== Ai Message ==================================

The result of the operations is 282.
"""