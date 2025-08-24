#!/usr/bin/python3
from typing import Annotated, Sequence, TypedDict
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage, AIMessage, ToolMessage
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
import os

load_dotenv()

api_key=os.getenv("OPENAI_API_KEY")

#create llm
llm=ChatOpenAI(
    model="gpt-4o",
    openai_api_key=api_key
)


# this global variable to store document content
document_content=""

#define the Graph schema
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage],add_messages]


#Now create the toool
@tool
def update(content: str)-> str:
    """Update the document with the provided content"""
    #interact with the global variable
    global document_content
    document_content=content
    return f"Document has been updated successfully! The current content is: \n{document_content}"

@tool
def save(filename: str)->str:
    """Save the current document to a text file and finish the process
    
    Args:
        filename: Name for the text file.
    """

    global document_content

    #handles if the file name has no .txt extension and adds it
    if not filename.endswith('.txt'):
        filename=f"{filename}.txt"

    #Now lets save the contents of the global variable under the text file provided
    try:
        with open(filename,'w')as file:
            file.write(document_content)
            print(f"\n Document has been saved to: {filename}")
            return f"Document has been saved successfully to '{filename}'"
        
    #if any error occurs during saving the file
    except Exception as e:
        return f"Error saving document: {str(e)}"
    
tools=[update, save]
model=llm

#bind our tools to the model
model.bind_tools(tools)


def our_agent(state: AgentState) -> AgentState:
    system_prompt = SystemMessage(content=f"""
        You are Drafter, a helpful writing assistant. You can ONLY modify the document by calling tools.

        Rules:
        - To update or modify content, ALWAYS call the 'update' tool with the complete updated content.
        - To save and finish, ALWAYS call the 'save' tool with the filename (e.g., 'meeting.txt').
        - Never just say "I saved it" — you MUST call the tool.
        - After each tool call, show the current document state.

        Current document content is: {document_content}
        """)

    if not state["messages"]:
        user_input = "I'm ready to help you update a document. What would you like to create?"
        user_message = HumanMessage(content=user_input)
    else:
        user_input = input("\nWhat would you like to do with the document? ")
        print(f"\n👤 USER: {user_input}")
        user_message = HumanMessage(content=user_input)

    all_messages = [system_prompt] + list(state["messages"]) + [user_message]

    response = model.invoke(all_messages)

    print(f"\n🤖 AI: {response.content}")
    if hasattr(response, "tool_calls") and response.tool_calls:
        print(f"🔧 USING TOOLS: {[tc['name'] for tc in response.tool_calls]}")

    return {"messages": list(state["messages"]) + [user_message, response]}


def should_continue(state: AgentState) -> str:
    """Determine if we should continue or end the conversation."""
    messages = state["messages"]
    
    if not messages:
        return "continue"
    
    # Check the last message to see if it's a tool call for save
    last_message = messages[-1]
    
    # If the AI message contains a save tool call
    if (isinstance(last_message, AIMessage) and 
        hasattr(last_message, "tool_calls") and 
        last_message.tool_calls):
        for tool_call in last_message.tool_calls:
            if tool_call["name"] == "save":
                return "end"
    
    # If we just executed a save tool and got the result
    if (isinstance(last_message, ToolMessage) and 
        "saved successfully" in last_message.content.lower()):
        return "end"
        
    return "continue"

def print_messages(messages):
    """Function I made to print the messages in a more readable format"""
    if not messages:
        return
    
    for message in messages[-3:]:
        if isinstance(message, ToolMessage):
            print(f"\n🛠️ TOOL RESULT: {message.content}")


graph = StateGraph(AgentState)

graph.add_node("agent", our_agent)
graph.add_node("tools", ToolNode(tools))

graph.set_entry_point("agent")

graph.add_edge("agent", "tools")


graph.add_conditional_edges(
    "tools",
    should_continue,
    {
        "continue": "agent",
        "end": END,
    },
)

app = graph.compile()

def run_document_agent():
    print("\n ===== DRAFTER =====")
    
    state = {"messages": []}
    
    for step in app.stream(state, stream_mode="values"):
        if "messages" in step:
            print_messages(step["messages"])
    
    print("\n ===== DRAFTER FINISHED =====")

if __name__ == "__main__":
    run_document_agent()