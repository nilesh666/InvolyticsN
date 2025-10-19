from pymongo import MongoClient
from pymongo.server_api import ServerApi
from utils.custom_exception import CustomException
from utils.logger import logging
import sys

class Operations:
    def __init__(self, uri: str, db_name: str):
        try:
            self.client = MongoClient(uri, server_api=ServerApi('1'))
            self.client.admin.command('ping')
            logging.info("MongoDB connection successful")
        except Exception as e:
            raise CustomException(e, sys)
        
        self.db = self.client[db_name]

    def insert(self, collection_name:str, data):
        try:
            collection = self.db[collection_name]
            result = collection.insert_many(data)
            logging.info(f"Data inserted with ids: {result.inserted_ids}")
            return result.inserted_ids
        except Exception as e:
            raise CustomException(e, sys)


    def delete(self, collection_name:str, data):
        try:
            collection = self.db[collection_name]
            result = collection.delete_many(data)
            logging.info(f"Documents deleted count: {result.deleted_count}")
            return result.deleted_count
        except Exception as e:
            raise CustomException(e, sys)
        
    
# if __name__ == "__main__":
#     from dotenv import load_dotenv
#     import os
#     load_dotenv()
#     uri = os.getenv("MONGO_URI")
#     instance = Operations(uri, "ImageProcessing")
#     print(instance)