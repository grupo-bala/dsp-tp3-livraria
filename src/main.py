from contextlib import asynccontextmanager
from fastapi import FastAPI
from .routes.customer import customer_router
from .database.connection import connect_db, close_db

DATABASE_URL = "mongodb://localhost:27017"
DATABASE_NAME = "meu_banco"

@asynccontextmanager
async def db_lifespan(app):
    await connect_db(DATABASE_URL, DATABASE_NAME)
    yield
    await close_db()

app = FastAPI(lifespan=db_lifespan)

app.include_router(customer_router)