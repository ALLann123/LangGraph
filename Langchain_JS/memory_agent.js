import { ChatGroq } from "@langchain/groq";
import 'dotenv/config';
import PromptSync from 'prompt-sync';
import { BufferMemory } from "langchain/memory";
import { ConversationChain } from "langchain/chains";

// input prompt
const prompt = PromptSync();

// LLM
const model = new ChatGroq({
    model: 'llama-3.3-70b-versatile',
    temperature: 0,
    apiKey: process.env.GROQ_API_KEY
});

// Memory (use `history` for ConversationChain)
const memory = new BufferMemory({
    returnMessages: true,
    memoryKey: "history"
});

// Build conversation chain (LLM + memory)
const chain = new ConversationChain({
    llm: model,
    memory
});

// Conversation function
async function conversation(humanInput) {
    const response = await chain.invoke({ input: humanInput });
    return response.response; // ConversationChain returns { response }
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
        console.log();
    }
}

main();


/*


You: What do you know about me?
AI: I know that your name is Allan, you're from Kenya, you're 25 years old, and you're currently unemployed. You've also mentioned that you have a strong interest in computers. That's the information you've shared with me so far, Allan. If you'd like to share more, I'm here to listen and chat with you.

You: quit

GoodBYe!!
*/