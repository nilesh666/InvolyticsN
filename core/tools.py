from agno.tools import tool
from mongo.files import FileHandler
from utils.config import mongo_uri, mongo_db_name
from utils.custom_exception import CustomException
import sys

@tool(name="fetch_raw_data_from_mongo", description="Fetches all raw file names that are unprocessed from the MongoDB 'raw' collection.")
def fetch_raw(collection_name="raw"):
    """
    Fetches file names of unporcessed/raw data from MongoDB. It returns a list of file names.
    """
    try:
        instance = FileHandler(mongo_uri, mongo_db_name)
        raw_data = instance.get_raw(collection_name)
        if not raw_data:
            return "Raw collection is empty"
        if isinstance(raw_data, list):
            return " ".join(map(str, raw_data))
        else:
            return f"Unspupported data format: {type(raw_data)}"
    except Exception as e:
        raise CustomException(e, sys)
    
@tool(name="fetch_local_raw_data", description="Fetches all raw file names from a local directory which are not loaded to MongoDB.")
def fetch_local_raw(collection_name="raw"):
    """
    Fetches file names of unporcessed/raw data from a local directory. It returns a list of file names.
    """
    from utils.config import local_folder_path
    try:
        instance = FileHandler(mongo_uri, mongo_db_name)
        raw_local_data = instance.get_local_raw(local_folder_path)
        raw_in_mongo = instance.get_raw(collection_name)
        if len(raw_local_data) == 0:
            return "Local directory is empty"
        if raw_local_data: 
            for i in raw_in_mongo:
                if i in raw_local_data:
                    raw_local_data.remove(i)
            return raw_local_data
        else:
            return "All files are loaded to MongoDB"
    except Exception as e:
        raise CustomException(e, sys)

@tool(name="fetch_processed_responses_from_mongo", description="Fetches all processed file responses from the '' MongoDB.")
def fetch_responses(collection_name="processed"):
    """
    Fetches processed file responses from MongoDB. It returns a list of all processed responses.
    """
    try:
        instance = FileHandler(mongo_uri, mongo_db_name)
        responses = instance.get_responses(collection_name)
        if responses:
            return responses
        else:
            return "Processed collection is empty"
    except Exception as e:
        raise CustomException(e, sys)


# if __name__ == "__main__":
#     l = fetch_local_raw(local_path=local_folder_path, collection_name="raw")
#     print(l)