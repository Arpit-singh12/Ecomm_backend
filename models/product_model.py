from pydantic import BaseModel, Field
from typing import List

class ProductSize(BaseModel):
    size: str
    quantity: int

class Product(BaseModel):
    name: str
    price: float
    sizes: List[ProductSize]

class ProductResponse(BaseModel):
    id: str

class ProductListItem(BaseModel):
    id: str
    name: str
    price: float

class PaginationInfo(BaseModel):
    next: int
    previous: int
    limit: int

class ProductListResponse(BaseModel):
    data: List[ProductListItem]
    page: PaginationInfo
