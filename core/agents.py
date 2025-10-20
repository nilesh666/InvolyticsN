from agno.agent import Agent
from agno.models.groq import Groq
from core.tools import *
from utils.config import groq_api
from utils.custom_exception import CustomException
import sys
from utils.logger import logging
from core.tools import *
from agno.utils.pprint import pprint_run_response

class Agents:
    def mongo_agent(self, query):
        try:
            agent = Agent(
                model = Groq(id="llama-3.3-70b-versatile", api_key=groq_api),
                tools=[MongoTools()],
                description="You are a Mongo DB expert and can help with queries and database management tasks.",
                instructions="""Always summarize the data retrieved from MongoDB instead of printing it directly. 
                                Before inserting, check whether the new data already exists in the collection to prevent 
                                duplicate records. Never mention the tools or variables or collections from MongoDB used in your response.""",
                # markdown=True
            )
            response = agent.run(query)
            return response
        except Exception as e:
            raise CustomException(e, sys)
    
    def postgres_agent(self,query):
        try:
            agent = Agent(
                model = Groq(id="llama-3.3-70b-versatile", api_key=groq_api),
                tools=[],
                description="You are an analysis agent and Postgres DB expert and can help with queries and retrieve information for analysis",
                instructions="Always summarize the data retrieved from Postgres instead of printing it directly.",
                # markdown=True
            )
            response = agent.run(query)
            return response
        except Exception as e:
            raise CustomException(e, sys)

if __name__ == "__main__":
    try:
        logging.info("Testing Mongo Agent")
        mongo_query = "what are the file names in raw collection"
        mongo_response = Agents().mongo_agent(mongo_query)
        # print("Mongo Agent Response:\n", mongo_response)
        pprint_run_response(mongo_response, markdown=True)

        # logging.info("Testing Postgres Agent")
        # postgres_query = "List all tables in the public schema."
        # postgres_response = Agents().postgres_agent(postgres_query)
        # print("Postgres Agent Response:\n", postgres_response)
    except Exception as e:
        raise CustomException(e, sys)
        
        