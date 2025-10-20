from pymongo import MongoClient
from pymongo.server_api import ServerApi
from utils.logger import logging
import sys
from utils.custom_exception import CustomException
import base64

class FileHandler:
    def __init__(self, uri: str, db_name: str):
        try:
            self.client = MongoClient(uri, server_api=ServerApi('1'))
            self.client.admin.command('ping')
            logging.info("MongoDB connection successful")
        except Exception as e:
            raise CustomException(e, sys)
        
        self.db = self.client[db_name]

    def get_raw(self,collection_name:str):
        try:
            collection = self.db[collection_name]
            all_raw_docs = collection.find({}, {'_id': 0, 'file_data': 0, 'file_id':0})
            raw_files = [i['file_name'] for i in all_raw_docs]
            return raw_files
        except Exception as e:
            raise CustomException(e, sys)
    
    def get_local_raw(self,local_path:str):
        try:
            import os
            files = os.listdir(local_path)
            return files
        except Exception as e:
            raise CustomException(e, sys)
    
    # def convert(self, file_path): 
    #     try:
    #         with open(file_path, "rb") as file:
    #             encoded_string = base64.b64encode(file.read()).decode('utf-8')
    #         return encoded_string
    #     except Exception as e:
    #         raise CustomException(e, sys)
    
    def get_responses(self, collection_name:str):
        try:
            collection = self.db[collection_name]
            vlm_all_docs = collection.find({}, {'_id': 0, 'file_id': 0})
            return list(vlm_all_docs)
        except Exception as e:
            raise CustomException(e, sys)
    
# if __name__ == "__main__":
#     from dotenv import load_dotenv
#     import os
#     load_dotenv()
#     local_path = os.getenv("LOCAL_FOLDER_PATH")
#     uri = os.getenv("MONGO_URI")
#     instance = FileHandler(uri, "ImageProcessing")
#     raw = instance.get_local_raw(local_path)
#     print("raw: ", raw)
    



