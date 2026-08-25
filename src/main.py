import os
import requests
from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

# Configure Tracer
provider = TracerProvider()
processor = BatchSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

app = FastAPI(title="OTel Demo Service")

# Instrument libraries
FastAPIInstrumentor.instrument_app(app)
RequestsInstrumentor().instrument()

@app.get("/")
def read_root():
    with tracer.start_as_current_span("root_handler"):
        return {"message": "Hello from OTel Demo"}

@app.get("/chained")
def call_downstream():
    with tracer.start_as_current_span("call_downstream"):
        # In a real demo, this calls another service. Mocking a local call.
        try:
            response = requests.get("http://localhost:8000/")
            return {"downstream_status": response.status_code, "downstream_data": response.json()}
        except Exception as e:
            return {"error": str(e)}
