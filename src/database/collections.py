from enum import Enum


class Collections(str, Enum):
    BOOK = "book"
    EDITION = "edition"
    CUSTOMER = "customer"
    EMPLOYEE = "employee"
    SALE = "sale"   
    