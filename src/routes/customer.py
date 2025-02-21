from fastapi import APIRouter, HTTPException, Query
from typing import Annotated, Optional
from ..models import Customer
from .utils import get_response_object, generate_filters

customer_router = APIRouter(prefix="/customers", tags=["Customers"])


@customer_router.post("")
async def create_customer(customer: Customer):
    return {"data": await customer.insert()}


@customer_router.get("")
async def get_customers(
    page: int,
    size: int,
    id: Optional[str] = None,
    first_name: Annotated[str | None, Query(min_length=1)] = None,
    last_name: Annotated[str | None, Query(min_length=1)] = None,
    phone_number: Annotated[str | None, Query(min_length=1)] = None,
    email: Annotated[str | None, Query(min_length=1)] = None,
    address: Annotated[str | None, Query(min_length=1)] = None,
    sort_by: Optional[str] = None,
    sort_order: Optional[str] = Query("asc", regex="^(asc|desc)$"),
):
    filters = generate_filters(locals().items())
    query = Customer.find(filters)

    if sort_by:
        sort_direction = 1 if sort_order == "asc" else -1
        query = query.sort((sort_by, sort_direction))

    total_count = await query.count()
    customers = await query.skip((page - 1) * size).limit(size).to_list()

    return get_response_object(customers, page, size, total_count)


@customer_router.put("/{id}")
async def update_customer(id: str, customer_update: Customer):
    customer = await Customer.get(id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    update_data = customer_update.dict(exclude_unset=True)
    await customer.set(update_data)

    return {"data": customer}


@customer_router.delete("/{id}")
async def delete_customer(id: str):
    customer = await Customer.get(id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    await customer.delete()
    return {"message": "Customer deleted successfully"}
