from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, get_db

from app.routers import (
    auth_router,
    health_router,
    alerts_router,
    websocket_router,
    astronaut_router,
    ai_router,
)

app = FastAPI(
    title="AstroHealth API",
    description="Astronaut Health Monitoring System API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routers
app.include_router(auth_router)
app.include_router(astronaut_router)
app.include_router(health_router)
app.include_router(alerts_router)
app.include_router(websocket_router)
app.include_router(ai_router)

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