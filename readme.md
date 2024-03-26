Welcome to the LLM + Knowledge Graph Movie Agent.

## Engine Underneath

The Agent can use any of the two model choices:
    - Ollama (Mistral 7B)
    - Open AI

The Movie toy dataset was used as to build the Neo4j vector index

The embeddings used for this project was HuggigngFace's "hkunlp/instructor-large", but feel free to replace with any Huggingface model.

If you'd like to use other embeddings such as OAI, etc make sure to reset the vector index in your graph DB.

The Agent uses RetrievalQA and GraphCypherQAChain to do the vector search and construct the Cypher statemet needed to query the database, and then uses create_react_agent to create the full agent with the selected LLM of choice.

Implemented CustomEmbeddings for HuggingFaceEmbeddings which allows to utilize models that cannot be used for created embeddings directly.

Agent uses ConversationBufferWindowMemory to maintain memory

## How to Run

- pip install -r requirements.txt
- Ollama comes in handy to test multiple custom LLMs. Download Ollama based on the instructions here: https://github.com/ollama/ollama 
    - Run the Ollama for Mistral using `ollama run mistral`. This will setup your Model
    - You should see the Llama icon on your Notification tray and you should be able to query it independantly. Its running!
- Add your necessary keys to keys.py (Kept it as explicit keys for now , but ENV vars for future).
- Important: Langchain has a bug in processing the Agent's output in its memory. So I customized one of its file, since there was no official fix. Make sure to replace langchain/chat_memory.py to your env's python package repo for langchain under: langchain/memory/chat_memory.py
- Make sure your Neo4J sandbox is setup with the Movie data and run some basic cypher queries to ensure everything is available.
- Run main.py

## What to Expect

- You will be prompted with two model choices(1,2).
- After selecting the number, the respective model will be used to initialize the agent pipeline.
- Enter 'quit' if you want to end the chat
- The Agent primarily focuses on the Vector Index to answer your queries. It has been Prompt designed that way. But as you continue pressing for information outside, it will use the LLM's base trained knowledge.
- Enter 'feedback' to enter into feedback mode and enter your instructions if you want to explicitly instruct the agent to do something. For Example, "Talk only about Girls no matter what movie genre the user requests", the agent will do so and priorotize your instructions.
- Very rarely, the agent might throw a 'something went wrong', try again.
- The agent verbose is on. So expect to see the background thought processes before seeing the final response. The final response is indicated by "AI: <text>"
- The Prompting in this project has been kept really simple for ease.
- Because of the nature of the models, prompts, sometimes the agent might run into a error loop, do ctrl + c and restart the agent.