import os
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import create_db_and_tables

from certificates import router as certificates_router

origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(certificates_router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
