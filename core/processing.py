from huggingface_hub import InferenceClient
from utils.config import *
from utils.custom_exception import CustomException
import sys
from utils.logger import logging

class ImageProcessor:
    def __init__(self, model_name="Qwen/Qwen2.5-VL-7B-Instruct", hf_token=hf_token, prompt=image_extraction_prompt):
        try:
            self.client = InferenceClient(model=model_name, token=hf_token)
            self.prompt = prompt
            logging.info(f"Connected to Hugging Face model: {model_name}") 
        except Exception as e:
            raise CustomException(e, sys)

    def process(self, image_base64):
        try:
            completion = self.client.chat.completions.create(
            model="Qwen/Qwen2.5-VL-7B-Instruct",
            messages=[
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": "Extract all the relevant fields from the image and give it in neat json format."
                                    },
                                    {
                                        "type": "image_url",
                                        "image_url":{
                                            "url": f"data:image/jpeg;base64,{image_base64}"
                                        }
                                    }
                                ]
                            }
                        ],
                    )
            response_text = completion.choices[0].message.content
            return response_text
        
        except Exception as e:
            raise CustomException(e, sys)
    

