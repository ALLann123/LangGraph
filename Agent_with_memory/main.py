#/usr/bin/python3
import os
from typing import TypedDict, List, Union
from langchain_core.messages import HumanMessage,AIMessage
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph,START,END
from dotenv import load_dotenv

#load our API keys
load_dotenv()

#create the graph schema
class AgentState(TypedDict):
    messages:List[Union[HumanMessage, AIMessage]]


#set up our LLM in our casee llama on groq 
llm = ChatGroq(
    temperature=0.3,  # Lower temperature for more factual responses
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile"
)


#create node
def process(state: AgentState)-> AgentState:
    """This node will solve the request you input"""
    #we pass our message History to the LLM
    response=llm.invoke(state["messages"])

    #now append the new message to the graph state
    state['messages'].append(AIMessage(content=response.content))
    print(f"\nAI: {response.content}")

    print("\n Current State: ", state['messages'])

    return state

#create the graph
graph=StateGraph(AgentState)

#add node
graph.add_node("process", process)

#add edges
graph.add_edge(START, "process")
graph.add_edge("process", END)

#compile our graph
agent=graph.compile()

#hold our chat history
conversation_history=[]


while True:
    user_input=input("\nUSER: ")

    if user_input in ['exit', 'quit']:
        break

    conversation_history.append(HumanMessage(content=user_input))
    #we invoke the agent by passing the human message to the agent
    result=agent.invoke({"messages": conversation_history})
    conversation_history=result["messages"]

    

"""

USER: hi

AI: It's nice to meet you. Is there something I can help you with or would you like to chat?

 Current State:  [HumanMessage(content='hi', additional_kwargs={}, response_metadata={}), AIMessage(content="It's nice to meet you. Is there something I can help you with or would you like to chat?", additional_kwargs={}, response_metadata={})]

"""