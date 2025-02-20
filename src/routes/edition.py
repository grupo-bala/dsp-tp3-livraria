from typing import Annotated, Optional
from fastapi import APIRouter, HTTPException, Query
from ..models import Edition
from .utils import get_response_object, generate_filters

edition_router = APIRouter(prefix="/editions", tags=["Editions"])

@edition_router.post("")
async def create_edition(edition: Edition):
    return {"data": await edition.insert()}

@edition_router.get("")
async def get_editions(
    page: int,
    size: int,
    id: Optional[str] = None,
    isbn: Annotated[str | None, Query(min_length=1)] = None,
    publisher: Annotated[str | None, Query(min_length=1)] = None,
    language: Annotated[str | None, Query(min_length=1)] = None,
    book_id: Optional[str] = None,
    sort_by: Optional[str] = None,
    sort_order: Optional[str] = Query("asc", regex="^(asc|desc)$"),
):
    filters = generate_filters(locals().items())
    query = Edition.find(filters)

    if sort_by:
        sort_direction = 1 if sort_order == "asc" else -1
        query = query.sort((sort_by, sort_direction))
    
    total_count = await query.count()
    editions = await query.skip((page - 1) * size).limit(size).to_list()

    return get_response_object(editions, page, size, total_count)


@edition_router.put("/{id}")
async def update_edition(id: str, edition_update: Edition):
    edition = await Edition.get(id)
    if not edition:
        raise HTTPException(status_code=404, detail="Edition not found")

    update_data = edition_update.dict(exclude_unset=True)
    await edition.set(update_data)

    return {"data": edition}


@edition_router.delete("/{id}")
async def delete_edition(id: str):
    edition = await Edition.get(id)
    if not edition:
        raise HTTPException(status_code=404, detail="Edition not found")

    await edition.delete()
    return {"message": "Edition deleted successfully"}
