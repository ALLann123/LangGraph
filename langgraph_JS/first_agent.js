import { ChatGroq } from "@langchain/groq";
import { TavilySearch } from "@langchain/tavily";
import { BaseCheckpointSaver, MemorySaver } from "@langchain/langgraph";
import { HumanMessage } from "@langchain/core/messages";
import { createReactAgent } from "@langchain/langgraph/prebuilt";
import "dotenv/config"


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

//invoke the agent
const agentFinalState = await agent.invoke({
    messages: [new HumanMessage("What is the current weather in sf")]
}, { configurable: { thread_id: "42" } }, );

//get the final message from the agent
console.log(
    agentFinalState.messages[agentFinalState.messages.length - 1].content,
);

/*
 node .\test_llm.js
The current weather in San Francisco is foggy with a temperature of 13.3°C (55.9°F) and a humidity of 93%. 
The wind is blowing at 2.7 mph (4.3 kph) from the SSW direction. The pressure is 1016.0 mb (30.0 in) and the cloud cover is 0%. 
The feels-like temperature is 13.7°C (56.6°F) and the wind chill is 12.5°C (54.5°F). 
The dew point is 12.5°C (54.4°F) and the visibility is 16.0 km (9.0 miles). 
The UV index is 0.0 and the gust wind speed is 5.0 mph (8.1 kph).

*/