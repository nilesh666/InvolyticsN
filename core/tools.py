from agno.tools import tool, Toolkit
from utils.config import mongo_uri, mongo_db_name
from utils.custom_exception import CustomException
import sys

class MongoTools(Toolkit):
    def __init__(self, **kwargs):
        super().__init__(name="mongo_tools", 
                         tools = [
                            self.fetch_raw,
                            self.fetch_local_raw,
                            self.fetch_responses,
                            self.load_local_to_mongo
                         ])
        
    # @tool(name="fetch_raw_data_from_mongo", description="Fetches all raw file names that are unprocessed from the MongoDB 'raw' collection.")
    def fetch_raw(self, collection_name="raw"):
        from mongo.files import FileHandler
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
        
    # @tool(name="fetch_local_raw_data", description="Fetches all raw file names from a local directory which are not loaded to MongoDB.")
    def fetch_local_raw(self, collection_name="raw"):
        from mongo.files import FileHandler
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
        
    # @tool(name="fetch_processed_responses_from_mongo", description="Fetches all processed file responses from the '' MongoDB.")
    def fetch_responses(self, collection_name="processed"):
        from mongo.files import FileHandler
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
            

    # @tool(name="load_local_to_mongo", description="Loads local files to MongoDB 'raw' collection.")
    def load_local_to_mongo(self,collection_name="raw"):
        """
        Loads local files to MongoDB 'raw' collection.

        Args:
            - file_names: list of file names to be loaded.
            - collection_name: name of the MongoDB collection (default is 'raw').
        """
        from utils.config import mongo_uri, mongo_db_name
        from mongo.operations import Operations
        from utils.config import local_folder_path
        import base64
        import os
        try:
            file_list = self.fetch_local_raw(collection_name)
            instance = Operations(mongo_uri, mongo_db_name)
            if not os.path.exists(local_folder_path):
                return f"Local path {local_folder_path} does not exist."
            
            if file_list and type(file_list)!=str:
                local_files_path=[os.path.join(local_folder_path, i) for i in file_list]
                converted_files = []
                for i in local_files_path:
                    d={}
                    d["file_name"]=os.path.basename(i)
                    d["file_data"]=base64.b64encode(open(i, "rb").read()).decode('utf-8')
                    converted_files.append(d)
                result = instance.insert(collection_name,converted_files) 
                return result
            else:
                return file_list
        except Exception as e:
            raise CustomException(e, sys)

class ProcessTool(Toolkit):
    def __init__(self, **kwargs):
        super().__init__(name="process_tools", 
                         tools = [
                            self.process_data,
                         ])

    def process_data(raw_collection="raw",processed_collection="processed"):
        from core.processing import ImageProcessor
        from mongo.files import FileHandler
        from mongo.operations import Operations
        """
        Processes the data from "raw" collection and stores it in "processed" collection. Do not change the input values for this function.

        Args:
            - raw_collection: "raw" (default)
            - processed_collection: "processed" (default)
        """
        file_instance=FileHandler(mongo_uri, mongo_db_name)
        raw_files = file_instance.get_raw(str(raw_collection))
        processed_files = file_instance.get_response_file_names(str(processed_collection))
        operation_instance = Operations(mongo_uri, mongo_db_name)
        processor = ImageProcessor()
        # print("raw_files:", raw_files)
        # print("processed_files:", processed_files)
        for i in raw_files:
            if i in processed_files:
                operation_instance.delete(processed_collection, {"file_name": i})
            data = {}
            vlm_response = processor.process(file_instance.get_file_data(i, raw_collection))
            data = {
                "file_name": i,
                "vlm_response": vlm_response
            }
            if data:
                operation_instance.insert(processed_collection, [data])
        
    

class AnalysisTool(Toolkit):
    pass

    #------------------Start working from here------------------

# if __name__ == "__main__":
#     try:
#         l,d = process_data()
#         print(l)
#         for i in d:
#             print(i["file_name"])
#     except Exception as e:
#         raise CustomException(e, sys)