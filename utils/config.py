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

#Gemini_API
gemini=os.getenv("GEMINI_API_KEY")

hf_token = os.getenv("HF_TOKEN")
groq_api = os.getenv("GROQ_API_KEY")
gemini_api = os.getenv("GEMINI_API_KEY")

mongo_uri = os.getenv("MONGO_URI")
mongo_db_name = os.getenv("MONGO_DB_NAME")

postgres_db=os.getenv("POSTGRES_DB")
postgres_user=os.getenv("POSTGRES_USER")
postgres_password=os.getenv("POSTGRES_PASSWORD")
postgres_host=os.getenv("POSTGRES_HOST")
postgres_port=os.getenv("POSTGRES_PORT")

local_folder_path = os.getenv("LOCAL_FOLDER_PATH")


