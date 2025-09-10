#!/usr/bin/python3
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGroq(
    temperature=0,
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-8b-instant"  # cheaper & lower quota usage
)



result=llm.invoke("Hello")

print(f"AI: {result.content}")

