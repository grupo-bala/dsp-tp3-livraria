from fastapi import APIRouter, HTTPException, Query
from typing import Annotated, Optional
from datetime import date
from ..models import Sale
from .utils import get_response_object, generate_filters

sale_router = APIRouter(prefix="/sales", tags=["Sales"])

@sale_router.post("")
async def create_sale(sale: Sale):
    return {"data": await sale.insert()}


@sale_router.get("")
async def get_sales(
    page: int,
    size: int,
    id: Optional[str] = None,
    customer_id: Optional[str] = None,
    employee_id: Optional[str] = None,
    payment_type: Annotated[str | None, Query(min_length=1)] = None,
    date: Optional[date] = None,
    sort_by: Optional[str] = None,
    sort_order: Optional[str] = Query("asc", regex="^(asc|desc)$"),
):
    filters = generate_filters(locals().items())
    query = Sale.find(filters)

    if sort_by:
        sort_direction = 1 if sort_order == "asc" else -1
        query = query.sort((sort_by, sort_direction))
    
    total_count = await query.count()
    sales = await query.skip((page - 1) * size).limit(size).to_list()

    return get_response_object(sales, page, size, total_count)


@sale_router.put("/{id}")
async def update_sale(id: str, sale_update: Sale):
    sale = await Sale.get(id)
    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")

    update_data = sale_update.dict(exclude_unset=True)
    await sale.set(update_data)

    return {"data": sale}


@sale_router.delete("/{id}")
async def delete_sale(id: str):
    sale = await Sale.get(id)
    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")

    await sale.delete()
    return {"message": "Sale deleted successfully"}
