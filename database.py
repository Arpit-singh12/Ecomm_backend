import os 
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

# Connect to MongoDB...
client = AsyncIOMotorClient(MONGO_URI)
db = client["ecommerce"]   # Database name...

# Collections...
product_collection = db["products"]  
order_collection = db["orders"]