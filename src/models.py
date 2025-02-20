from datetime import date
from typing import List, Optional
from beanie import Document


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
    book_id: str
    

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
    edition_id: str


class Sale(Document):
    date: date
    payment_type: str
    customer_id: str
    employee_id: str
    items: List[SaleItem]