from fastapi import APIRouter
from typing import List
from pydantic import BaseModel
from models.model import classify_text

router = APIRouter()

class BatchInput(BaseModel):
    text: List[str]


@router.post("/predict")
def predict(input: BatchInput):
    labels = [classify_text(text) for text in input.text]
    return {"labels": labels}
