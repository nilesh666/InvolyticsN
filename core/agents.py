from agno.agent import Agent
from agno.models.groq import Groq
from agno.models.google import Gemini
from core.tools import *
from utils.config import groq_api, gemini_api
from utils.custom_exception import CustomException
import sys
from utils.logger import logging
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
                                Use only "process_data" tool to process the data. 
                                Use "fetch_local_raw tool to list the file names that are not loaded to the "raw" collection.
                                Use fetch_raw tool to list the raw file names that are not processed.
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
                tools=[AnalyticsTool()],
                description="""You are an analysis agent and Postgres DB expert and can help with queries and retrieve information for analysis,
                                 never execute CRUD operations on the DB.
                                 You have access to a table called sales_data.
                                 The sales_data table has 9 columns that are:
                                    - "file_name": contains the name of the invoice/bill
                                    - "invoice_number": unique number identification for the respective invoice
                                    - "seller_name": name of the seller in the invoice
                                    - "client_name": name of the client in the invoice,
                                    - "date_of_issue": issued date of the invoice,
                                    - "vat_percentage": value added tax percentage in the invoice/bill,
                                    - "net_worth": total cost of items before taxes in the invoice/bill,
                                    - "vat": value added tax amount in the invoice/bill,
                                    - "gross_worth": the total amount for the invoice/bill
                                generate a query for the follwoing user query based on the given table description.
                                With the generated query use analyse tool to get the contents from the db""",
                                    instructions="Always summarize the data retrieved from Postgres instead of printing it directly. If you don't know or the query returns nothing simply print sorry i am not able to answer it",
                # markdown=True
            )
            response = agent.run(query)
            return response
        except Exception as e:
            raise CustomException(e, sys)

if __name__ == "__main__":
    try:
        logging.info("Testing Mongo Agent")
        # mongo_query = "Process the files"""
        # mongo_response = Agents().mongo_agent(mongo_query)
        # print("Mongo Agent Response:\n", mongo_response)
        postgres_query="Who sold the highest"
        postgres_response=Agents().postgres_agent(postgres_query)
        pprint_run_response(postgres_response, markdown=True)

        # logging.info("Testing Postgres Agent")
        # postgres_query = "List all tables in the public schema."
        # postgres_response = Agents().postgres_agent(postgres_query)
        # print("Postgres Agent Response:\n", postgres_response)
    except Exception as e:
        raise CustomException(e, sys)
        
        