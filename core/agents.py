from agno.agent import Agent
from agno.models.groq import Groq
from core.tools import *
from utils.config import groq_api
from utils.custom_exception import CustomException
import sys
from utils.logger import logging

class Agents:
    def mongo_agent(self, query):
        try:
            agent = Agent(
                model = Groq(id="llama-3.3-70b-versatile", api_key=groq_api),
                tools=[],
                description="You are a Mongo DB expert and can help with queries and database management tasks.",
                instructions="Always summarize the data retrieved from MongoDB instead of printing it directly. Before inserting, check whether the new data already exists in the collection to prevent duplicate records.",
                markdown=True
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
                markdown=True
            )
            response = agent.run(query)
            return response
        except Exception as e:
            raise CustomException(e, sys)
        
        