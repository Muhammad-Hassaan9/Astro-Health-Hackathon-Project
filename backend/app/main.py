from fastapi import FastAPI

from sqlalchemy import text
from app.database import engine

from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import get_db

app = FastAPI(title="AstroHealth API")

@app.get("/")
def home():
    return {"message": "Welcome to AstroHealth API"}

@app.get("/db-check")
def database_check():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    return {"database": "connected"}

@app.get("/db-session-check")
def db_session_check(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"database_session": "working"}