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

#set up our LLM in our case llama on groq 
llm = ChatGroq(
    temperature=0.3,  # Lower temperature for more factual responses
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile"
)

#structured output parser- LLM to give us an output that matches our exact output here. Useful for conditional edges
class MessageClassifier(BaseModel):
    #we set to get an exact value
    message_type: Literal["emotional","logical"]=Field(
        ...,
        description="Classify if the message requires an emotional (therapist) or logical response"
    )

#state graph schema- Control the flow of our application
class State(TypedDict):
    #store new messages from the user and the LLM. Annotated we take two inputs. add_messages appends to our state new message
    messages: Annotated[list, add_messages]
    message_type: str | None

#make node
def classify_message(state: State):
    #we get the last message (LangChain HumanMessage object)
    last_message = state["messages"][-1]
    #set llm to give us an output that matches the pydantic class above
    classifier_llm = llm.with_structured_output(MessageClassifier)

    #take user message and classify
    result = classifier_llm.invoke([
        {
            "role":"system",
            "content":"""Classify the user message as either:
            - 'emotional': if it asks for emotional support, therapy, deals with feelings, or personal problems
            - 'logical': if it asks for facts, information, logical analysis, or practical solutions
            """
        },
        {
            #get the last message from the user
            "role":"user",
            "content": last_message.content
        }
    ])

    #we update the message type to update a state in our schema
    return {"message_type": result.message_type}

#ROUTER
def router(state: State) -> str:
    #we get the message classified and if not classified by default we go logical
    message_type = state.get("message_type", "logical")

    if message_type == "emotional":
        return {"next":"therapist"}
    
    #this is the else if the above if statement turns false
    return {"next":"logical"}

def therapist_agent(state: State):
    #get the last message (HumanMessage)
    last_message = state['messages'][-1]

    messages = [{
        'role':"system",
        "content":"""You are a compassionate therapist. Focus on the emotional aspects of the user's message.
                        Show empathy, validate their feelings, and help them process their emotions.
                        Ask thoughtful questions to help them explore their feelings more deeply.
                        Avoid giving logical solutions unless explicitly asked."""
        },
        {
        'role':'user',
        'content': last_message.content
        }
    ]

    #pass in the input
    reply = llm.invoke(messages)
    return {"messages":[{'role':"assistant","content":"[Therapist_Agent]"+reply.content}]}

def logical_agent(state: State):
    #get the last message (HumanMessage)
    last_message = state['messages'][-1]

    messages = [{
        'role':"system",
        "content":"""You are a purely logical assistant. Focus only on facts and information.
            Provide clear, concise answers based on logic and evidence.
            Do not address emotions or provide emotional support.
            Be direct and straightforward in your responses."""
        },
        {
        'role':'user',
        'content': last_message.content
        }
    ]

    #pass in the input
    reply = llm.invoke(messages)
    return {"messages":[{'role':"assistant","content":"[Logical_Agent]"+reply.content}]}

#Make the graph
graph_builder = StateGraph(State)

#add a node
graph_builder.add_node("classifier", classify_message)
graph_builder.add_node("router", router)
graph_builder.add_node("therapist", therapist_agent)
graph_builder.add_node("logical", logical_agent)

#add edges
graph_builder.add_edge(START, end_key="classifier")
graph_builder.add_edge("classifier", "router")

#add conditional edge
graph_builder.add_conditional_edges(
    "router",
    lambda state: state.get('next'),
    {"therapist":"therapist","logical":"logical"}
)

graph_builder.add_edge("therapist", END)
graph_builder.add_edge("logical", END)

#compile the graph
graph = graph_builder.compile()

def run_chatbot():
    state = {"messages":[],"message_type":None}

    while True:
        user_input = input("Message: ")

        if user_input == "exit":
            print('Bye')
            break

        #we get the current messages in the graph and add the user input message
        state["messages"] = state.get("messages",[]) + [
            {"role":"user","content":user_input}
        ]

        state = graph.invoke(state)

        if state.get("messages") and len(state["messages"])>0:
            last_message = state["messages"][-1]

            #if last_message is a dict (our assistant reply), use ['content'], else fallback to .content
            if isinstance(last_message, dict):
                print(f"Assistant: {last_message['content']}")
            else:
                print(f"Assistant: {last_message.content}")

if __name__=='__main__':
    run_chatbot()


"""
 python .\main.py
Message: hey, I am sad
Assistant: I'm so sorry to hear that you're feeling sad. It can be really tough to navigate those emotions. Would you like to talk about what's on your mind and what might be contributing to your sadness? Sometimes sharing your feelings with someone who cares can help you feel a little better. I'm here to listen and support you.

How are you taking care of yourself right now, and is there anything in particular that's feeling overwhelming or weighing on your heart?
Message: quite
Assistant: It seems like you're feeling a bit reserved or perhaps overwhelmed at the moment. Would you like to talk about what's on your mind, or is it more about taking a moment to breathe and gather your thoughts? Sometimes, just acknowledging our emotions can be a powerful step in understanding ourselves better. How are you feeling right now?
Message: exit
"""