import { ChatGroq } from "@langchain/groq";
import { TavilySearch } from "@langchain/tavily";
import { MemorySaver } from "@langchain/langgraph";
import { HumanMessage } from "@langchain/core/messages";
import { createReactAgent } from "@langchain/langgraph/prebuilt";
import "dotenv/config";
import { writeFileSync } from "node:fs";

// Define LLM
const model = new ChatGroq({
    model: "llama-3.3-70b-versatile",
    temperature: 0,
    apiKey: process.env.GROQ_API_KEY,
});

// Define search tool
const tavily = new TavilySearch({
    apiKey: process.env.TAVILY_API_KEY,
    maxResults: 3,
});

// Initialize memory
const agentCheckpointer = new MemorySaver();

// Create the agent
const agent = createReactAgent({
    llm: model,
    tools: [tavily],
    checkpointSaver: agentCheckpointer,
});

// Invoke the agent
const agentFinalState = await agent.invoke({
    messages: [new HumanMessage("What is the current weather in Kenya?")],
}, { configurable: { thread_id: "42" } });

// Get the final message
console.log(
    "Agent response:",
    agentFinalState.messages[agentFinalState.messages.length - 1].content
);

// --- Visualize the graph workflow ---
const graph = agent.getGraph(); // ✅ access graph instance
const graphStateImage = await graph.drawMermaidPng(); // ✅ draw diagram
const arrayBuffer = await graphStateImage.arrayBuffer();

const filePath = "./graphState.png";
writeFileSync(filePath, new Uint8Array(arrayBuffer));
console.log("✅ Saved agent graph diagram:", filePath);
/**
  node .\test_llm.js
Agent response: The current weather in Kenya is partly cloudy with a temperature of 24.3°C (75.7°F) in Nairobi, with a wind speed of 9.2 mph (14.8 kph) and a humidity of 47%. The weather forecast for Kisumu County on August 30, 2025, is expected to be 63°F (17°C) at 0:00 with a 50% probability of precipitation and a wind speed of 2 mph (3.2 kph) from the east.
✅ Saved agent graph diagram: ./graphState.png
 */