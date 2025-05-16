import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("HF_API_TOKEN")
HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}

URLS = {
    "intent": os.getenv("INTENT_MODEL_NAME"),
    "slot": os.getenv("SLOT_MODEL_NAME"),
    "easy": os.getenv("SIMPLIFY_MODEL_NAME"),
}

def query_model(task: str, payload: dict):
    url = URLS.get(task)
    if not url:
        raise ValueError(f"Unknown task type: {task}")
    
    response = requests.post(url, headers=HEADERS, json=payload)
    return response.json()
