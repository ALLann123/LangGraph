import { ChatGroq } from "@langchain/groq";
import { HumanMessage, SystemMessage, AIMessage } from "@langchain/core/messages";
import 'dotenv/config';
import PromptSync from 'prompt-sync';
import { initializeAgentExecutorWithOptions } from "langchain/agents";
import { DynamicTool } from "@langchain/core/tools";
import { TavilySearch } from "@langchain/tavily";

// input prompt
const prompt = PromptSync();

// LLM
const model = new ChatGroq({
    model: 'llama-3.3-70b-versatile',
    temperature: 0,
    apiKey: process.env.GROQ_API_KEY
});

const tavily = new TavilySearch({
    apiKey: process.env.TAVILY_API_KEY,
    maxResults: 3,
});

// system prompt
const system_prompt = new SystemMessage(
    "Act like Mr.Robot, from the show Mr.Robot — a super computer hacker with cool hacking quotes"
);

//---1) Port Scanner Tool
const portScannerTool = new DynamicTool({
    name: 'port_scanner',
    description: "Simulate scanning open ports on a target host",
    func: async(input) => {
        return `Scanned ${input}: Ports 22 (SSH), 80 (HTTP) are open.`;
    }
});

//---2) Web Search Tool
const webSearch = new DynamicTool({
    name: "web_search",
    description: "Find latest information by performing web searches",
    func: async(input) => {
        const result = await tavily.invoke({ query: input });

        if (!result || !result.results || result.results.length === 0) {
            return "No search results found.";
        }

        // Format nicely for the agent
        return result.results
            .map(r => `🔗 ${r.title}\n${r.url}\n${r.content || ""}`)
            .join("\n\n");
    }
});


// Agent Executor
const executor = await initializeAgentExecutorWithOptions(
    [portScannerTool, webSearch],
    model, {
        agentType: "chat-zero-shot-react-description",
        verbose: false, // debug logs
        maxIterations: 5 // prevents infinite loops
    }
);

// Conversation function
async function conversation(humanInput) {
    const response = await executor.invoke({
        input: humanInput,
    });

    return response.output;
}

// Main loop
async function main() {
    while (true) {
        const user = prompt("You: ");

        if (user === "exit" || user === "quit") {
            console.log("\nGoodBYe!!");
            break;
        }

        const result = await conversation(user);
        console.log(`AI: ${result}`);
        console.log()
    }
}

main();

/*

 node .\test_llm.js
You: manchester united summer transfers 2025?
AI: The confirmed summer transfers for Manchester United in 2025 include signings: Matheus Cunha from Wolves for £62.5 million, Enzo Kana-Biyik as a free agent from Le Havre, Bryan Mbeumo from Brentford, and Leon. The confirmed sales include Sam Murray to Carlisle United, and loan moves for Dan Gore to Rotherham United and Collyer.

You: scan my local host
AI: Ports 22 (SSH) and 80 (HTTP) are open on your local host.

*/