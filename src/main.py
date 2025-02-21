import os
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from fastapi import FastAPI
from .database.connection import connect_db, close_db
from .routes.customer import customer_router
from .routes.book import book_router
from .routes.edition import edition_router
from .routes.employee import employee_router
from .routes.sale import sale_router
from .routes.sale_item import sale_item_router

load_dotenv()

@asynccontextmanager
async def db_lifespan(app):
    await connect_db(os.getenv("DATABASE_URL"))
    yield
    await close_db()

app = FastAPI(lifespan=db_lifespan)

app.include_router(customer_router)
app.include_router(book_router)
app.include_router(edition_router)
app.include_router(employee_router)
app.include_router(sale_router)
app.include_router(sale_item_router)