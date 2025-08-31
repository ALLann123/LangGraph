import { TavilySearch } from "@langchain/tavily";
import 'dotenv/config';

const webSearch = new TavilySearch({
    apiKey: process.env.TAVILY_API_KEY,
    maxResults: 3,
});

//call the tool above
const result = await webSearch.invoke({
    query: "Whos is the founder of OpenAI"
});
console.log(result);

/*


node .\search_tool.js
{
  query: 'Whos is the founder of OpenAI',
  follow_up_questions: null,
  answer: null,
  images: [],
  results: [
    {
      url: 'https://en.wikipedia.org/wiki/OpenAI',
      title: 'OpenAI - Wikipedia',
      content: 'In December 2015, OpenAI was founded as a not for profit organization by Sam Altman, Elon Musk, Ilya Sutskever, Greg Brockman, Trevor Blackwell, Vicki Cheung, Andrej Karpathy, Durk Kingma, John Schulman, Pamela Vagata, and Wojciech Zaremba, with Sam Altman and Elon Musk as the co-chairs. | Products | | Chatbots | * ChatGPT * in education * GPT Store * DALL-E * ChatGPT Search * Sora "Sora (text-to-video model)") * Whisper "Whisper (speech recognition system)") * GitHub Copilot | | --- | | Foundation models | * OpenAI Codex * Generative pre-trained transformer * GPT-1 * GPT-2 * GPT-3 * GPT-4 * GPT-4o * o1 * o3 * GPT-4.5 * GPT-4.1 * o4-mini * GPT-OSS * GPT-5 | | Intelligent agents | * ChatGPT Deep Research * Operator | | Image 18.svg) |',
      score: 0.91118777,
      raw_content: null
    },
    {
      url: 'https://observer.com/2024/07/openai-founders-career/',
      title: "Only 4 of OpenAI's 11 Founders Are Still With the Company—Where ...",
      content: 'At the time of OpenAI’s founding, Altman juggled his duties as co-chair of the company and as the president of the startup accelerator Y Combinator. Before co-founding OpenAI, Greg Brockman was the chief technology officer of the fintech company Stripe. Earlier this year, Musk sued OpenAI and Altman, claiming that the company prioritizes profit over its original mission to benefit humanity in a lawsuit that has since been dropped. Business, Artificial Intelligence, Technology, Trevor Blackwell, Vicki Cheung, Durk Kingma, Pamela Vagata, Josh Tobin, Geoff Ralston, Wojciech Zaremba, John Schulman, Patrick Collison, Jan Leike, Greg Brockman, Andrej Karpathy, Yann LeCun, Ilya Sutskever, Reid Hoffman, Geoffrey Hinton, Peter Thiel, Sam Altman, ChatGPT, Elon Musk, Google, Google DeepMind, Lyft, Meta, OpenAI, Stripe, Tesla, xAI, Y Combinator',
      score: 0.82048416,
      raw_content: null
    },
    {
      url: 'https://www.britannica.com/money/OpenAI',
      title: 'OpenAI | ChatGPT, Sam Altman, Microsoft, & History - Britannica',
      content: 'OpenAI | ChatGPT, Sam Altman, Microsoft, & History | Britannica Money Sam Altman is CEO of OpenAI, the artificial intelligence company that developed ChatGPT. OpenAI is an American artificial intelligence (AI) research organization consisting of two entities: OpenAI Inc., a nonprofit research segment, and OpenAI Global LLC, a for-profit subsidiary established to commercialize its AI technologies and applications. As OpenAI continued developing its AI 
technologies, it learned that its anticipated cost of production would exceed the capital it was able to raise through standard nonprofit channels. This third iteration—among the most advanced AI models for processing language and generating human-like text—would later power OpenAI’s flagship ChatGPT platform. Also in May, OpenAI released ChatGPT-4o (“omni”), which can process and generate text, images, and audio in real time—a type of AI known as a multimodal model.',
      score: 0.80698997,
      raw_content: null
    }
  ],
  response_time: 1.35,
  request_id: '39609060-e061-4188-934d-b723f5cd808a'
}
*/