from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import Tool
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate
from langchain.chains import GraphCypherQAChain
from langchain.chains import RetrievalQA

from langchain_community.embeddings import HuggingFaceEmbeddings

from Prompts import BasePrompt
from keys import Keys
from graph import Graph
# from customEmbeddings import HuggingFaceEmbeddings
from models import Model

import datetime


class MovieAgent:

    def __init__(self) -> None:
        self.userInstructions = ''

    def initialize(self, model: str) -> bool:
        try:
            self.keys = Keys()

            self.new_graph = Graph(
                uri=self.keys.NEO4J_URI,
                username=self.keys.NEO4J_USERNAME,
                password=self.keys.NEO4J_PASSWORD,
            )
            self.new_graph.initGraph()

            self.modelObj = Model()
            if model == 'OLL':   
                self.modelObj.Ollama(modelName="mistral")
                embeddings = HuggingFaceEmbeddings(model_name=self.keys.HUGGING_FACE_EMBEDDING)
            else:
                self.modelObj.OpenAI(self.keys.OPENAI_API_KEY)
                embeddings = HuggingFaceEmbeddings(model_name=self.keys.HUGGING_FACE_EMBEDDING)
            
            self.neo4jvector = self.new_graph.getNeo4jVector(
                                    embeddings,
                                    indexName="MoviePlot",
                                    nodeLabel='Movie',
                                    nodeProperties=["title","tagline","released"],
                                    columnName="plotEmbedding"           
                                    )
            
            self.prompter = BasePrompt()
            return True
        except Exception as e:
            print(e)
            return

    def setupPipeline(self) -> None:
        graphInstance = self.new_graph.getGraph()
        retriever = self.neo4jvector.as_retriever()
        llm = self.modelObj.getModel()

        self.agent_prompt = PromptTemplate.from_template(self.prompter.agentPrompt)
        self.cypher_prompt = PromptTemplate.from_template(self.prompter.cypherPrompt)

        kg_qa = RetrievalQA.from_llm(
            llm,                  
            # chain_type="stuff",  
            retriever=retriever, 
        )
        cypher_qa = GraphCypherQAChain.from_llm(
            llm,
            graph=graphInstance,
            verbose=True,
            cypher_prompt=self.cypher_prompt
        )

        tools = [
            Tool.from_function(
                name="Vector Search Index",
                description="Provides information about movie data using Vector Search", 
                func = kg_qa,
                return_direct=True
                ),
            Tool.from_function(
                name="Graph Cypher QA Chain", 
                description="Provides  information about Movies only present in the database. Return a proper Cypher query", 
                func = cypher_qa,
                return_direct=True
                ),
                ]
        memory = ConversationBufferWindowMemory(
            memory_key='chat_history',
            k=5,
            return_messages=True,
        )

        agent = create_react_agent(llm, tools, self.agent_prompt)
        self.agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            memory=memory,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=10 #Note: Remove if the llm breaks early
            )

    def generate_response(self, prompt: str) -> str:
        """
        Create a handler that calls the Conversational agent
        and returns a response
        """
        response = self.agent_executor.invoke({"input": prompt})
        response = response.get('output')
        if isinstance(response, dict):
            return response['result']
        else:
            return response



if __name__ == '__main__':
    modelSelection = input("\n Select a Model to start with \n1.Ollama (Mistral) \n2.OpenAI \n User: ")
    if modelSelection == '1':
        selectedModel = 'OLL'
    else:
        selectedModel = 'OAI'

    print('Setting up the Reels')
    movieagent = MovieAgent()
    status = movieagent.initialize(model=selectedModel)

    if status:
        movieagent.setupPipeline()
        print('Setup Complete!')

        curTime = None
        while True:
            if not curTime:
                curTime = datetime.datetime.now()
                user_input = input("{} AI: Whatsup Mate. Watcha want \n User: ".format(str(curTime.strftime("%Y-%m-%d %H:%M:%S"))))
            else:
                curTime = datetime.datetime.now()
                user_input = input("\n User: ")
            if not user_input:
                continue
            if user_input == 'quit':
                response = "Ciao!"
                break
            if user_input == 'feedback':
                user_instruction = input("I'm listening.... \n User: ")
                movieagent.userInstructions += '\n - ' + user_instruction
                print('Got it!')
                continue

            try:
                addOn = ''
                if movieagent.userInstructions:
                    addOn = 'Follow these Instructions strictly:\n' + movieagent.userInstructions
                modifiedInput = user_input + '\n' + addOn
                response = movieagent.generate_response(modifiedInput)
            except Exception as e:
                print(e)
                print("Something went wrong can you try again....")
                continue
            
            curTime = datetime.datetime.now()
            print(curTime.strftime("%Y-%m-%d %H:%M:%S") + ' AI: ' + response)