from fastapi import APIRouter
from typing import List
from pydantic import BaseModel
from pymongo import MongoClient
from hashlib import sha256
from ..models.model import classify_text
import os
from dotenv import load_dotenv

load_dotenv()

# Connect to MongoDB
client = MongoClient(os.getenv("MONGO_URI"))  
db = client.ResumeLogs
collection = db.ApiLogs

router = APIRouter()

class BatchInput(BaseModel):
    text: List[str]

# Mapping the labels
label_map = {
    "Edu": "Education",
    "Exp": "Experience",
    "Skill": "Skills",
    "Obj": "Objective",
    "QC": "Qualifications and Certificates",
    "PI": "Personal Information",
    "Sum": "Summary"
}
    


@router.post("/predict")
def predict(input: BatchInput):
    labels = []
    new_entries = []
    # print(os.getenv("MONGO_URI"))
    for text in input.text:
        label = classify_text(text)
        labels.append(label)
        mapped_label = label_map[label]
    mapped_labels = [label_map[label] for label in labels]        

    #     # Create a hash of the text
    #     input_hash = sha256(text.encode()).hexdigest()

    #     # Check if this hash already exists in the DB
    #     if not collection.find_one({"input_hash": input_hash}):
    #         # Prepare the document to insert
    #         print("find_one completed")
    #         new_entries.append({
    #             "input": text,
    #             "label": label,
    #             "input_hash": input_hash
    #         })

    # # Bulk insert all new (unique) entries
    # if new_entries:
    #     collection.insert_many(new_entries)
    # print(mapped_labels, labels)
    return {"labels": mapped_labels}
