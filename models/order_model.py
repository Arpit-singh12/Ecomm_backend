from pydantic import BaseModel, Field
from typing import List

class OrderItem(BaseModel):
    productID: str = Field(
        ...,
        example="687af97656fdd012aafe0472",
        pattern="^[a-fA-F0-9]{24}$",  # Valid ObjectId string
        description="MongoDB ObjectId as a 24-character hex string"
    )
    qty: int = Field(..., gt=0, example=3)

class Order(BaseModel):
    userId: str = Field(..., example="user_1")
    items: List[OrderItem]

class OrderResponse(BaseModel):
    id: str