from huggingface_hub import InferenceClient
from utils.config import *
from utils.custom_exception import CustomException
from typing import List, Annotated
import sys
from utils.logger import logging
from pydantic import BaseModel, Field, PositiveInt
from datetime import date
from decimal import Decimal
import json

class InvoiceInfo(BaseModel):
    number: PositiveInt=Field(None, description="Invoice number")    
    date_of_invoice: date=Field(None, json_schema_extra= {"description": "Invoice date in YYYY-MM-DD format"})

class Seller(BaseModel):
    name: str = Field(None, json_schema_extra= {"description": "Seller's name"})
    address: str = Field(None, json_schema_extra= {"description": "Seller's address"})
    tax_id: str = Field(None, json_schema_extra= {"description": "Tax id"})
    iban: str = Field(None, json_schema_extra={"description":"International Bank account number"})

class Client(BaseModel):
    name: str=Field(None, json_schema_extra={"description": "Client's name"})
    address: str = Field(None, json_schema_extra={"description":"Client's address"})
    tax_id: str=Field(None, json_schema_extra={"description": "Tax id"})

class Item(BaseModel):
    number: PositiveInt=Field(None, json_schema_extra={"description":"Item number"})
    description: str=Field(None, json_schema_extra={"descritpion":"Description of the product or service"})
    quantity: PositiveInt=Field(None, json_schema_extra={"description":"Qunatity purchased"})
    unit: str=Field(None, json_schema_extra={"description": "Describes how much for each"})
    net_price: Annotated[Decimal, Field(strict=True, allow_inf_nan=True, json_schema_extra={"description":"Price per unit before vat"})]
    net_worth: Annotated[Decimal, Field(strict=True, allow_inf_nan=True, json_schema_extra={"description" :"Total net worth"})]
    vat_percentage: Annotated[Decimal, Field(strict=True, allow_inf_nan=True, json_schema_extra={"description":"vat percentage"})]
    gross_worth: Annotated[Decimal, Field(strict=True, allow_inf_nan=True, json_schema_extra={"description": "Total of the product including everything"})]

class Summary(BaseModel):
    vat_percentage: Annotated[Decimal, Field(strict=True, allow_inf_nan=True,json_schema_extra={"description":"vat percentage"})]
    net_worth:  Annotated[Decimal, Field(strict=True, allow_inf_nan=True, json_schema_extra={"description": "Total net worth"})]
    vat:  Annotated[Decimal, Field(strict=True, allow_inf_nan=True)]
    gross_worth:  Annotated[Decimal, Field(strict=True, allow_inf_nan=True,json_schema_extra={"description":"Final total including everything"})]

class Invoice(BaseModel):
    seller: Seller
    client: Client
    invoice: InvoiceInfo  
    items: List[Item]
    summary: Summary

    class ConfigDict:
        json_schema_extra = {
            "example": {
                "invoice": {"number": "51109338", "date": "2013-04-13"},
                "seller": {
                    "name": "Andrews, Kirby and Valdez",
                    "address": "58861 Gonzalez Prairie, Lake Daniellefurt, IN 57228",
                    "tax_id": "945-82-2137",
                    "iban": "GB75MCRL06841367619257"
                },
                "client": {
                    "name": "Becker Ltd",
                    "address": "8012 Stewart Summit Apt. 455, North Douglas, AZ 95355",
                    "tax_id": "942-80-0517"
                },
                "items": [
                    {
                        "number": 1,
                        "description": "CLEARANCE! Fast Dell Desktop Computer PC DUAL CORE WINDOWS 10 4/8/16GB RAM",
                        "quantity": 3.00,
                        "unit": "each",
                        "net_price": 209.00,
                        "net_worth": 627.00,
                        "vat_percentage": 10,
                        "gross_worth": 689.70
                    }
                ],
                "summary": {
                    "vat_percentage": 10,
                    "net_worth": 5640.17,
                    "vat": 564.02,
                    "gross_worth": 6204.19
                }
            }
        }

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
                    response_format={
                        "type": "json_schema",
                        "json_schema": {
                            "title": "Invoice",
                            "schema": Invoice.model_json_schema()
                        }
                    }
                    )
            response_text = completion.choices[0].message.content
            return response_text
        
        except Exception as e:
            raise CustomException(e, sys)
    
if __name__=="__main__":
    schema = Invoice.model_json_schema()
    print(json.dumps(schema, indent=2))
    

