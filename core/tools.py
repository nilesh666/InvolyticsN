from agno.tools import tool
from mongo.files import FileHandler
from utils.config import mongo_uri, mongo_db_name
from utils.custom_exception import CustomException
import sys

@tool(name="fetch_raw_data_from_mongo", description="Fetches all raw file names that are unprocessed from the MongoDB 'raw' collection.")
def fetch_raw():
    """
    Fetches file names of unporcessed/raw data from MongoDB. It returns a list of file names.
    """
    try:
        instance = FileHandler(mongo_uri, mongo_db_name)
        raw_data = instance.get_raw()
        return raw_data
    except Exception as e:
        raise CustomException(e, sys)
    
@tool(name="fetch_local_raw_data", description="Fetches all raw file names from a local directory which are not loaded to MongoDB.")
def fetch_local_raw():
    """
    Fetches file names of unporcessed/raw data from a local directory. It returns a list of file names.
    """
    from utils.config import local_folder_path
    import os

    try:
        instance = FileHandler(mongo_uri, mongo_db_name)
        raw_local_data = instance.get_local_raw(local_folder_path)
        raw_in_mongo = instance.get_raw("raw")
        for i in raw_in_mongo:
            if i in raw_local_data:
                raw_local_data.remove(i)
        return raw_local_data
    except Exception as e:
        raise CustomException(e, sys)

@tool(name="fetch_processed_responses_from_mongo", description="Fetches all processed file responses from the '' MongoDB.")
def fetch_responses():
    """
    Fetches processed file responses from MongoDB. It returns a list of all processed responses.
    """
    try:
        instance = FileHandler(mongo_uri, mongo_db_name)
        responses = instance.get_responses("processed")
        return responses
    except Exception as e:
        raise CustomException(e, sys)


