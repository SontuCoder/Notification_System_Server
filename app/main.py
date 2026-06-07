from app.core.config import settings
from fastapi import FastAPI  # type: ignore[import]
from app.core.database import check_database_connection

app = FastAPI()
@app.get("/")
def root():
    return {"message": "Notification Service"}

check_database_connection()