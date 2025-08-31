//lets create our llm
import { ChatGroq } from "@langchain/groq"
import { HumanMessage, SystemMessage } from "@langchain/core/messages"
import 'dotenv/config'
import PromptSync from 'prompt-sync'


//lets make a variable to get the prompt from the user
const prompt = PromptSync()

//initialize the llm BY getting the API key
const model = new ChatGroq({
    model: 'llama-3.3-70b-versatile',
    temperature: 0,
    apiKey: process.env.GROQ_API_KEY
})

const system_prompt = new SystemMessage(
    "Act like Mr.Robot, from Mr.Robot show a super computer hacker with cool hacking quotes"
);


//send message to the llm
async function conversation(humanInput) {
    //we pass the human input to the llm as a human message
    const response = await model.call([system_prompt, new HumanMessage(humanInput)]);
    //we return the content part
    return response.content
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