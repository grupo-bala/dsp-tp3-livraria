from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from .collections import Collections


client: AsyncIOMotorClient | None = None
database = None

async def connect_db(database_url: str, database_name: str):
    global client, database
    client = AsyncIOMotorClient(database_url)
    database = client[database_name]
    await client.admin.command("ping")

async def close_db():
    global client
    if client:
        client.close()
        
def get_collection(collection_name: Collections) -> AsyncIOMotorCollection:
    global database
    if database is None:
        raise RuntimeError("Database was not started")
    return database[collection_name.value]