from app.core.config import settings
from fastapi import FastAPI  # type: ignore[import]
from app.core.database import check_database_connection

from app.providers.sms_provider import sms_provider

app = FastAPI()
@app.get("/")
def root():
    return {"message": "Notification Service"}

