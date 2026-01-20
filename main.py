from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI

from database import create_db_and_tables

from certificates import router as certificates_router

app = FastAPI()

app.include_router(certificates_router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
