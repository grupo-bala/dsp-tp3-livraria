from fastapi import APIRouter
from ..database.collections import Collections
from ..database.crud import create
from ..database.connection import get_collection
from ..models import Customer

customer_router = APIRouter(prefix="/customers", tags=["Customers"])

@customer_router.post("")
async def create_customer(customer: Customer):
    customer_collection = get_collection(Collections.CUSTOMER)
    customer_data = customer.model_dump(exclude_unset=True)
    result = await create(customer_collection, customer_data)
    return result

@customer_router.get("/count")
async def count():
    return {"count": await get_collection(Collections.CUSTOMER).count_documents({})}