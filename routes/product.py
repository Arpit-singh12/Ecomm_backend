from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from models.product_model import Product, ProductResponse, ProductListResponse, ProductListItem, PaginationInfo
from database import product_collection
from bson import ObjectId
import re

router = APIRouter()

# Helper to convert Mongo _id to string and flatten product
def serialize_product(product) -> ProductListItem:
    return ProductListItem(
        id=str(product["_id"]),
        name=product["name"],
        price=product["price"]
    )

@router.post("/products", response_model=ProductResponse, status_code=201)
async def create_product(product: Product):
    new_product = await product_collection.insert_one(product.dict())
    return {"id": str(new_product.inserted_id)}

@router.get("/products", response_model=ProductListResponse)
async def list_products(
    name: Optional[str] = None,
    size: Optional[str] = None,
    limit: int = Query(10, ge=1),
    offset: int = Query(0, ge=0)
):
    query = {}

    if name:
        query["name"] = {"$regex": name, "$options": "i"}

    if size:
        query["sizes.size"] = size  # Check if any size object has matching size

    total_products = product_collection.find(query)
    cursor = total_products.skip(offset).limit(limit)

    products = []
    async for doc in cursor:
        products.append(serialize_product(doc))

    return {
        "data": products,
        "page": {
            "next": offset + limit,
            "previous": max(offset - limit, 0),
            "limit": len(products)
        }
    }
