// test_llm.mjs

import { ChatGroq } from "@langchain/groq";
import { TavilySearch } from "@langchain/tavily";
import { HumanMessage, SystemMessage, AIMessage } from "@langchain/core/messages";
import { ToolNode } from "@langchain/langgraph/prebuilt";
import { StateGraph, MessagesAnnotation } from "@langchain/langgraph";
import "dotenv/config";

// 1. Tools
const tools = [
    new TavilySearch({ apiKey: process.env.TAVILY_API_KEY, maxResults: 3 }),
];
const toolNode = new ToolNode(tools);

// 2. LLM with tool binding
const model = new ChatGroq({
    model: "llama-3.3-70b-versatile",
    temperature: 0,
    apiKey: process.env.GROQ_API_KEY,
}).bindTools(tools);

// 3. Decide whether to continue
function shouldContinue({ messages }) {
    const lastMessage = messages[messages.length - 1];

    if (lastMessage.tool_calls ? .length) {
        console.log("➡️ AI decided to call tool:", lastMessage.tool_calls);
        return "tools";
    }

    return "__end__";
}

// 4. Agent node
async function callModel(state) {
    const response = await model.invoke(state.messages);
    return { messages: [response] };
}

// 5. Graph
const workflow = new StateGraph(MessagesAnnotation)
    .addNode("agent", callModel)
    .addNode("tools", toolNode)
    .addEdge("__start__", "agent")
    .addConditionalEdges("agent", shouldContinue)
    .addEdge("tools", "agent"); // important: go back to agent after tools run

// 6. Compile runnable
const app = workflow.compile();

// 7. Run once
const finalState = await app.invoke({
    messages: [
        new SystemMessage(
            "You are an assistant. If you don't know the answer, ALWAYS use the web search tool before responding."
        ),
        new HumanMessage("How much was stolen from Ecitizen platform in Kenya in 2025?"),
    ],
});

// 8. Print result
console.log(
    "\n🤖 Final AI Response:",
    finalState.messages[finalState.messages.length - 1].content
);


/*
 node .\test_llm.js
➡️ AI decided to call tool: [
  {
    name: 'tavily_search',
    args: {
      query: 'Current deputy president of Kenya',
      searchDepth: 'basic',
      topic: 'general'
    },
    type: 'tool_call',
    id: 'sqbjcrp4c'
  }
]

🤖 Final AI Response: The current deputy president of Kenya is Kithure Kindiki. He has been serving in this position since 1 November 2024.
*/