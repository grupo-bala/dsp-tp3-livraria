from typing import Annotated, Optional
from fastapi import APIRouter, HTTPException, Query
from ..models import Book
from .utils import get_response_object, generate_filters

book_router = APIRouter(prefix="/books", tags=["Books"])


@book_router.post("")
async def create_book(book: Book):
    return {"data": await book.insert()}


@book_router.get("")
async def get_books(
    page: int,
    size: int,
    id: Optional[str] = None,
    title: Annotated[str | None, Query(min_length=1)] = None,
    author: Annotated[str | None, Query(min_length=1)] = None,
    language: Annotated[str | None, Query(min_length=1)] = None,
    genre: Annotated[str | None, Query(min_length=1)] = None,
    sort_by: Optional[str] = None,
    sort_order: Optional[str] = Query("asc", regex="^(asc|desc)$"),
):
    filters = generate_filters(locals().items())
    query = Book.find(filters)

    if sort_by:
        sort_direction = 1 if sort_order == "asc" else -1
        query = query.sort((sort_by, sort_direction))

    total_count = await query.count()
    books = await query.skip((page - 1) * size).limit(size).to_list()

    return get_response_object(books, page, size, total_count)


@book_router.put("/{id}")
async def update_book(id: str, book_update: Book):
    book = await Book.get(id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    update_data = book_update.dict(exclude_unset=True)
    await book.set(update_data)

    return {"data": book}


@book_router.delete("/{id}")
async def delete_book(id: str):
    book = await Book.get(id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    await book.delete()
    return {"message": "Book deleted successfully"}
