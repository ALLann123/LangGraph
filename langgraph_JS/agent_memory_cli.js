import { ChatGroq } from "@langchain/groq";
import { TavilySearch } from "@langchain/tavily";
import { BaseCheckpointSaver, MemorySaver } from "@langchain/langgraph";
import { HumanMessage } from "@langchain/core/messages";
import { createReactAgent } from "@langchain/langgraph/prebuilt";
import "dotenv/config"
import PromptSync from 'prompt-sync';

//build prompt for keyboard input
const prompt = PromptSync();

//define llm
const model = new ChatGroq({
    model: 'llama-3.3-70b-versatile',
    temperature: 0,
    apiKey: process.env.GROQ_API_KEY
});

//Define the search tool
const tavily = new TavilySearch({
    apiKey: process.env.TAVILY_API_KEY,
    maxResults: 3,
})

//initialize memory to persist state between graph runs
const agentCheckpointer = new MemorySaver();

//now create the agent
const agent = createReactAgent({
    llm: model,
    tools: [tavily],
    checkpointSaver: agentCheckpointer,
})


while (true) {
    let user_input = prompt("You: ");

    if (user_input === "exit" || user_input === "quit") {
        console.log("Bye!!")
        break;
    };

    //invoke the agent
    const agentFinalState = await agent.invoke({
        messages: [new HumanMessage(user_input)]
    }, { configurable: { thread_id: "42" } }, );

    //get the final message from the agent
    console.log(
        `AI: ${agentFinalState.messages[agentFinalState.messages.length - 1].content}`
    );
    console.log();
}
/**
 You: Whats my name, and where did I study?
AI: Your name is Allan, and you studied at JKUAT (Jomo Kenyatta University of Agriculture and Technology) in the IT (Information Technology) department.

You: where am I currently?
AI: You are currently in Nairobi, Kenya, and you mentioned that you are currently unemployed.

You: where is Rigathi Gachagua currently?
AI: Rigathi Gachagua is currently in Kenya, having returned from a 43-day tour of the United States. He was welcomed back at Jomo Kenyatta International Airport (JKIA) and is expected to resume his duties as the Deputy President of Kenya.

You: exit
Bye!!
 */