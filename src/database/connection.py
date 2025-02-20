from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from ..models import Book, Edition, Employee, SaleItem, Sale, Customer

client: AsyncIOMotorClient | None = None

async def connect_db(database_url: str):
    global client
    client = AsyncIOMotorClient(database_url)
    await init_beanie(database=client.db_name, document_models=[Book, Edition, Employee, SaleItem, Sale, Customer])
    await client.admin.command("ping")


async def close_db():
    global client
    if client:
        client.close()