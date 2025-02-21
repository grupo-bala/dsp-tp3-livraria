from datetime import date
from typing import List, Optional
from beanie import Document, Link
from pydantic import BaseModel


class Book(Document):
    title: str
    publication_date: date
    language: str
    author: str
    genre: str


class Edition(Document):
    isbn: str
    price: float
    publisher: str
    language: str
    publication_year: int
    stock: int
    book: Link[Book]


class Customer(Document):
    first_name: str
    last_name: str
    phone_number: str
    email: str
    address: str


class Employee(Document):
    first_name: str
    last_name: str
    register_code: int
    hired_date: date
    wage: float


class SaleItem(Document):
    quantity: int
    discount: float
    is_gift: bool
    notes: Optional[str]
    edition: Link[Edition]


class Sale(Document):
    date: date
    payment_type: str
    customer: Link[Customer]
    employee: Link[Employee]
    items: List[Link[SaleItem]]


class SalesInTimeWindow(BaseModel):
    total: float
    total_quantity: int

    class Settings:
        projection = {
            "total": {
                "$sum": {
                    "$map": {
                        "input": "$items",
                        "as": "item",
                        "in": {
                            "$multiply": [
                                "$$item.quantity",
                                {
                                    "$divide": [
                                        {"$subtract": [100, "$$item.discount"]},
                                        100,
                                    ]
                                },
                                "$$item.edition.price",
                            ]
                        },
                    }
                }
            },
            "total_quantity": {
                "$sum": {
                    "$map": {"input": "$items", "as": "item", "in": "$$item.quantity"}
                }
            },
        }


class EditionsPriceSum(BaseModel):
    total: float

    class Settings:
        projection = {"total": {"$sum": "$price"}}
