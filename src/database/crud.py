from typing import Any, Dict, List, Optional
from motor.motor_asyncio import AsyncIOMotorCollection
from bson import ObjectId


async def create(collection: AsyncIOMotorCollection, document: dict) -> dict:
    result = await collection.insert_one(document)
    document["_id"] = str(result.inserted_id)
    
    return document

async def get_by_id(collection: AsyncIOMotorCollection, document_id: ObjectId) -> Optional[dict]:
    document = await collection.find_one({"_id": document_id})
    
    if document:
        document["_id"] = str(document["_id"])
        
    return document

async def update(collection: AsyncIOMotorCollection, document_id: ObjectId, update_data: dict) -> Optional[dict]:
    result = await collection.update_one({"_id": document_id}, {"$set": update_data})
    
    if result.modified_count == 0:
        return None
    
    return {**update_data, "_id": document_id}

async def delete(collection: AsyncIOMotorCollection, document_id: ObjectId) -> bool:
    result = await collection.delete_one({"_id": document_id})
    
    return result.deleted_count > 0

async def count(collection: AsyncIOMotorCollection) -> int:
    result = await collection.count_documents({})   
    
    return result