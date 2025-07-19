from fastapi import FastAPI
from routes import product, order

app = FastAPI(
    title="E-Commerce Backend",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {"message": "E-Commerce Backend API is running."}


# Product route...
app.include_router(product.router)

# Order route...
app.include_router(order.router)
