#!/usr/bin/python3
import os
from dotenv import load_dotenv
from typing import TypedDict, Annotated, Sequence
from operator import add as add_messages

from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.messages import (
    BaseMessage, HumanMessage, AIMessage, ToolMessage, SystemMessage
)
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END

# === Load Environment Variables ===
load_dotenv()

# === 1. Set up LLM (LLaMA on Groq) ===
llm = ChatGroq(
    temperature=0,
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile"
)

# === 2. Set up Embeddings ===
embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2",
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': False}
)

# === 3. Load and Split PDF ===
pdf_path = "Stock_Market_Performance_2024.pdf"
if not os.path.exists(pdf_path):
    raise FileNotFoundError(f"PDF not found: {pdf_path}")

pdf_loader = PyPDFLoader(pdf_path)
pages = pdf_loader.load()
print(f"PDF loaded: {len(pages)} pages")

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
docs = splitter.split_documents(pages)

# === 4. Store in Chroma ===
vectorstore = Chroma.from_documents(docs, embeddings, persist_directory="./chroma_db")
retriever = vectorstore.as_retriever()

# === 5. Define Tool ===
@tool
def retriever_tool(query: str) -> str:
    """
    Search and return info from the Stock Market Performance 2024 document.
    """
    docs = retriever.invoke(query)
    if not docs:
        return "No relevant information found in the Stock Market Performance 2024 document."

    results = []
    for i, doc in enumerate(docs):
        results.append(f"Document {i+1}:\n{doc.page_content}")
    return "\n\n".join(results)

tools = [retriever_tool]
tools_dict = {tool.name: tool for tool in tools}

# Bind tools to LLM
llm_with_tools = llm.bind_tools(tools)

# === 6. Define Agent State ===
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

system_prompt = (
    "You are a financial research assistant. "
    "Use the provided tools to answer questions about the Stock Market Performance 2024 document. "
    "If a tool is needed, call it. If not, answer directly."
)

# === 7. LLM Node ===
def call_llm(state: AgentState) -> AgentState:
    messages = [SystemMessage(content=system_prompt)] + list(state["messages"])
    message = llm_with_tools.invoke(messages)
    return {"messages": state["messages"] + [message]}

# === 8. Tool Node ===
def take_action(state: AgentState) -> AgentState:
    tool_calls = state["messages"][-1].tool_calls
    results = []

    for t in tool_calls:
        print(f"Calling Tool: {t['name']} with query: {t['args'].get('query', '')}")

        if t["name"] not in tools_dict:
            tool_result = "Incorrect Tool Name. Please retry with available tools."
        else:
            tool_result = tools_dict[t["name"]].invoke(t["args"])

        results.append(ToolMessage(content=tool_result, tool_call_id=t["id"]))

    return {"messages": state["messages"] + results}

# === 9. Router (decides next step) ===
def router(state: AgentState) -> str:
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "action"
    return END

# === 10. Build Graph ===
workflow = StateGraph(AgentState)
workflow.add_node("llm", call_llm)
workflow.add_node("action", take_action)
workflow.set_entry_point("llm")

workflow.add_conditional_edges("llm", router, {"action": "action", END: END})
workflow.add_edge("action", "llm")

app = workflow.compile()

# === 11. Run Example ===
if __name__ == "__main__":
    user_input = "Summarize the key highlights from the Stock Market Performance 2024 report."
    inputs = {"messages": [HumanMessage(content=user_input)]}

    print(f"🧑 User: {user_input}\n")

    try:
        # Use invoke instead of stream for better debugging
        result = app.invoke(inputs)
        
        # Print all messages in the final result
        for msg in result["messages"]:
            role = msg.__class__.__name__.replace("Message", "")
            content = msg.content
            if hasattr(msg, 'tool_calls') and msg.tool_calls:
                content += f"\nTool calls: {msg.tool_calls}"
            print(f"{role}: {content}\n")
            
    except Exception as e:
        print(f"Error occurred: {e}")
        import traceback
        traceback.print_exc()