from dotenv import load_dotenv
import os
import base64
from openinference.instrumentation.agno import AgnoInstrumentor
from opentelemetry import trace as trace_api
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor

load_dotenv()

# Set environment variables for Langfuse
LANGFUSE_AUTH = base64.b64encode(
    f"{os.getenv('LANGFUSE_PUBLIC_KEY')}:{os.getenv('LANGFUSE_SECRET_KEY')}".encode()
).decode()
os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = "https://cloud.langfuse.com/api/public/otel"
os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = f"Authorization=Basic {LANGFUSE_AUTH}"

# Configure the tracer provider
tracer_provider = TracerProvider()
tracer_provider.add_span_processor(SimpleSpanProcessor(OTLPSpanExporter()))
trace_api.set_tracer_provider(tracer_provider=tracer_provider)

# Start instrumenting agno
AgnoInstrumentor().instrument()

hf_token = os.getenv("HF_TOKEN")
groq_api = os.getenv("GROQ_API_KEY")
gemini_api = os.getenv("GEMINI_API_KEY")

mongo_uri = os.getenv("MONGO_URI")
mongo_db_name = os.getenv("MONGO_DB_NAME")

local_folder_path = os.getenv("LOCAL_FOLDER_PATH")

image_extraction_prompt = """
You are an intelligent document extraction assistant.
Your goal is to extract all relevant information from the given invoice (in text or image form) and return the output in strict JSON format.
Follow these rules carefully:
    - Follow the exact JSON structure below — do not change field names or hierarchy.
    - If any field is missing, return an empty string ("") for that field.
    - All numeric fields should be converted to numbers (no quotes), unless missing.
    - Return only the JSON. Do not include any explanation or text.
{
  "invoice_number": "",
  "date_of_issue": "",
  "seller": {
    "name": "",
    "address": "",
    "tax_id": "",
    "iban": ""
  },
  "client": {
    "name": "",
    "address": "",
    "tax_id": ""
  },
  "items": [
    {
      "no": 0,
      "description": "",
      "quantity": 0,
      "unit_of_measurement": "",
      "net_price": 0,
      "net_worth": 0,
      "vat_percentage": 0,
      "gross_worth": 0
    }
  ],
  "summary": {
    "vat_percentage": 0,
    "net_worth": 0,
    "vat": 0,
    "gross_worth": 0
  }
}
"""
