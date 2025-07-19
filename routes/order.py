from fastapi import APIRouter, HTTPException, Query, Path
from typing import List
from models.order_model import Order, OrderResponse
from database import order_collection, product_collection
from bson import ObjectId

router = APIRouter()

@router.post("/orders", response_model=OrderResponse, status_code=201)
async def create_order(order: Order):
    order_dict = order.model_dump()
    for item in order_dict["items"]:
        item["productID"] = ObjectId(item["productID"])
    new_order = await order_collection.insert_one(order_dict)
    return {"id": str(new_order.inserted_id)}

def fix_object_ids(order):
    # Convert top-level _id
    if "_id" in order:
        order["_id"] = str(order["_id"])
    # Convert productDetails.ID if present
    if "items" in order:
        for item in order["items"]:
            if "productDetails" in item and "ID" in item["productDetails"]:
                item["productDetails"]["ID"] = str(item["productDetails"]["ID"])
    return order

@router.get("/orders/{user_id}")
async def list_orders(
    user_id: str = Path(...),
    limit: int = Query(10, ge=0),
    offset: int = Query(0, ge=0)
):
    try:
        pipeline = [
            {"$match": {"userId": user_id}},
            {"$unwind": "$items"},
            {
                "$lookup": {
                    "from": "products",
                    "localField": "items.productID",
                    "foreignField": "_id",
                    "as": "product_details"
                }
            },
            {"$unwind": {"path": "$product_details", "preserveNullAndEmptyArrays": True}},
            {
                "$group": {
                    "_id": "$_id",
                    "items": {
                        "$push": {
                            "productDetails": {
                                "name": "$product_details.name",
                                "ID": "$product_details._id"
                            },
                            "qty": "$items.qty"
                        }
                    },
                    "total": {
                        "$sum": {
                            "$multiply": [
                                {"$ifNull": ["$product_details.price", 0]},
                                {"$ifNull": ["$items.qty", 0]}
                            ]
                        }
                    }
                }
            },
            {"$skip": offset},
            {"$limit": limit}
        ]

        orders = []
        async for order in order_collection.aggregate(pipeline):
            # objectId to string conversion
            orders.append(fix_object_ids(order))  

        return {
            "data": orders,
            "page": {
                "next": offset + limit,
                "previous": max(offset - limit, 0),
                "limit": limit
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))