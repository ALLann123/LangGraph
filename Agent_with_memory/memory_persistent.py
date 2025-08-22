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

# hold our chat history
conversation_history: List[Union[HumanMessage, AIMessage]] = []

# --- Load previous conversation if logging.txt exists
if os.path.exists("logging.txt"):
    with open("logging.txt", "r") as file:
        lines = file.readlines()

    for line in lines:
        line = line.strip()
        if line.startswith("You: "):
            conversation_history.append(HumanMessage(content=line.replace("You: ", "")))
        elif line.startswith("AI: "):
            conversation_history.append(AIMessage(content=line.replace("AI: ", "")))

    if conversation_history:
        print("[+] Loaded previous conversation from logging.txt")

while True:
    user_input=input("\nUSER: ")

    if user_input in ['exit', 'quit']:
        break

    conversation_history.append(HumanMessage(content=user_input))
    #we invoke the agent by passing the human message to the agent
    result=agent.invoke({"messages": conversation_history})
    conversation_history=result["messages"]

#---Check the log.txt file for conversation history
with open('logging.txt', 'w') as file:
    file.write("Your Conversation Log:\n")

    for message in conversation_history:
        if isinstance(message, HumanMessage):
            file.write(f"You: {message.content}\n")

        if isinstance(message,AIMessage):
            file.write(f"AI: {message.content}\n\n")

print("[+]Conversation saved to Logging.txt")



"""
python .\memory_persistent.py
[+] Loaded previous conversation from logging.txt

USER: Hi, what is my name?

AI: Your name is Allan, and you're from Kenya!

USER: What else do you know about me?

AI: Let me see... I know that:

1. Your name is Allan.
2. You're from Kenya.
3. You're 21 years old.

"""