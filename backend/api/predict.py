from fastapi import APIRouter
from typing import List
from pydantic import BaseModel
from pymongo import MongoClient
from hashlib import sha256
from models.model import classify_text
import os
from dotenv import load_dotenv

load_dotenv()

# Connect to MongoDB
client = MongoClient(os.getenv("MONGO_URI"))  # store safely using env vars
db = client.ResumeLogs
collection = db.ApiLogs

router = APIRouter()

class BatchInput(BaseModel):
    text: List[str]


@router.post("/predict")
def predict(input: BatchInput):
    labels = []
    new_entries = []

    for text in input.text:
        label = classify_text(text)
        labels.append(label)

        # Create a hash of the text
        input_hash = sha256(text.encode()).hexdigest()

        # Check if this hash already exists in the DB
        if not collection.find_one({"input_hash": input_hash}):
            # Prepare the document to insert
            new_entries.append({
                "input": text,
                "label": label,
                "input_hash": input_hash
            })

    # Bulk insert all new (unique) entries
    if new_entries:
        collection.insert_many(new_entries)

    return {"labels": labels}
