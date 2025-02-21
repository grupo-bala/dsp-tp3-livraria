from fastapi import APIRouter, HTTPException, Query
from typing import Annotated, Optional
from ..models import SaleItem
from .utils import get_response_object, generate_filters

sale_item_router = APIRouter(prefix="/sale-items", tags=["Sale Items"])


@sale_item_router.post("")
async def create_sale_item(sale_item: SaleItem):
    return {"data": await sale_item.insert()}


@sale_item_router.get("")
async def get_sale_items(
    page: int,
    size: int,
    id: Optional[str] = None,
    edition_id: Optional[str] = None,
    quantity: Optional[int] = None,
    discount: Optional[float] = None,
    is_gift: Optional[bool] = None,
    notes: Annotated[str | None, Query(min_length=1)] = None,
    sort_by: Optional[str] = None,
    sort_order: Optional[str] = Query("asc", regex="^(asc|desc)$"),
):
    filters = generate_filters(locals().items())
    query = SaleItem.find(filters)

    if sort_by:
        sort_direction = 1 if sort_order == "asc" else -1
        query = query.sort((sort_by, sort_direction))

    total_count = await query.count()
    sale_items = await query.skip((page - 1) * size).limit(size).to_list()

    return get_response_object(sale_items, page, size, total_count)


@sale_item_router.put("/{id}")
async def update_sale_item(id: str, sale_item_update: SaleItem):
    sale_item = await SaleItem.get(id)
    if not sale_item:
        raise HTTPException(status_code=404, detail="Sale Item not found")

    update_data = sale_item_update.dict(exclude_unset=True)
    await sale_item.set(update_data)

    return {"data": sale_item}


@sale_item_router.delete("/{id}")
async def delete_sale_item(id: str):
    sale_item = await SaleItem.get(id)
    if not sale_item:
        raise HTTPException(status_code=404, detail="Sale Item not found")

    await sale_item.delete()
    return {"message": "Sale Item deleted successfully"}
