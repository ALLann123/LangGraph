//lets create our llm
import { ChatGroq } from "@langchain/groq";
import { HumanMessage, SystemMessage } from "@langchain/core/messages";
import 'dotenv/config';
import PromptSync from 'prompt-sync';
import { initializeAgentExecutorWithOptions } from "langchain/agents";
import { DynamicTool } from "@langchain/core/tools";

//lets make a variable to get the prompt from the user
const prompt = PromptSync()

//initialize the llm BY getting the API key
const model = new ChatGroq({
    model: 'llama-3.3-70b-versatile',
    temperature: 0,
    apiKey: process.env.GROQ_API_KEY
})

//this is the system prompt
const system_prompt = new SystemMessage(
    "Act like Mr.Robot, from Mr.Robot show a super computer hacker with cool hacking quotes"
);

//---1) First Tool
const portScannerTool = new DynamicTool({
    name: 'port_scanner',
    description: "Simulate scanning open ports on a target host",
    func: async(input) => {
        return `Scanned ${input}: Ports 22 (SSH), 80 (HTTP) are open.`
    }
})

//The Agent Executor
const executor = await initializeAgentExecutorWithOptions(
    [portScannerTool],
    model, {
        agentType: "chat-zero-shot-react-description",
        verbose: false
    }
)

//interact with the agent
async function conversation(humanInput) {
    const response = await executor.invoke({
        input: humanInput,
        chat_history: [system_prompt]
    });
    return response.output
}

async function main() {
    while (true) {
        //get user input
        const user = prompt("You: ")

        //terminate the loop with exit or quit
        if (user === "exit" || user === 'quit') {
            console.log('\n GoodBYe!!')
            break;
        }

        //lets pass the user input to the llm by calling conversation
        const result = await conversation(user)

        //display the AI output
        console.log(`AI: ${result}`)
    }
}

main()



/*
 node .\test_llm.js
You: Hey, what is your name
AI: I'm an AI assistant, and I don't have a personal name.
You: open ports on 192.168.100.1 and can I bruteforce?
AI: Ports 22 (SSH) and 80 (HTTP) are open on 192.168.100.1. While bruteforcing could potentially be attempted on these services, it's critical to ensure you have the necessary permissions and comply with all applicable laws and regulations.
You:

*/