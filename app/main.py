from app.core.config import settings
from app.utils.logger import logger
from fastapi import FastAPI  # type: ignore[import]

app = FastAPI()
@app.get("/")
def root():
    return {"message": "Notification Service"}


