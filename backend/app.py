from fastapi import FastAPI
from .api import predict

app = FastAPI(title="Resume Classifier API")

app.include_router(predict.router)