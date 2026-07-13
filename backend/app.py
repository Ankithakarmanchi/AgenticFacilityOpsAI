from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from core.agent_loader import register_all_agents

load_dotenv()

app = FastAPI(
    title=os.getenv("APP_NAME"),
    version=os.getenv("APP_VERSION"),
    description="Agentic AI Facility Operations Platform API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
def home():
    return {
        "application": os.getenv("APP_NAME"),
        "version": os.getenv("APP_VERSION"),
        "status": "Running"
    }


@app.get("/health")
def health():
    return {"status": "Healthy"}


register_all_agents(app)