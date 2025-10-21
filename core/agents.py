from agno.agent import Agent
from agno.models.groq import Groq
from agno.models.google import Gemini
from core.tools import *
from utils.config import groq_api, gemini_api
from utils.custom_exception import CustomException
import sys
from utils.logger import logging
from core.tools import *
from agno.utils.pprint import pprint_run_response
from agno.guardrails import PIIDetectionGuardrail, PromptInjectionGuardrail

class Agents:
    def mongo_agent(self, query):
        try:
            agent = Agent(
                model = Groq(id="llama-3.3-70b-versatile", api_key=groq_api),
                tools=[MongoTools(), ProcessTool()],
                reasoning_model=Gemini(
                        id="gemini-2.5-flash", thinking_budget=1024, api_key=gemini_api,
                    ),
                description="You are a Mongo DB expert and can help with queries and database management tasks.",
                instructions="""Always provide a concise summary of data retrieved from MongoDB rather than displaying it directly.
                                Before adding any new records to the "raw" collection, verify whether the data already exists in the collection to avoid duplicate entries. If duplicates are found, skip insertion.
                                Do not mention any internal tools, variables, or collection names related to MongoDB in your responses.
                                If asked for sensitive information, politely decline to disclose it.
                                Use ProcessTool only to exclusively extract and process content from images.
                                Store processed outputs in the "processed" collection and raw data in the "raw" collection within MongoDB.
                                """,
                pre_hooks = [PIIDetectionGuardrail(), PromptInjectionGuardrail()],
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
        mongo_query = "Process the files"
        mongo_response = Agents().mongo_agent(mongo_query)
        # print("Mongo Agent Response:\n", mongo_response)
        pprint_run_response(mongo_response, markdown=True)

        # logging.info("Testing Postgres Agent")
        # postgres_query = "List all tables in the public schema."
        # postgres_response = Agents().postgres_agent(postgres_query)
        # print("Postgres Agent Response:\n", postgres_response)
    except Exception as e:
        raise CustomException(e, sys)
        
        