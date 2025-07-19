from fastapi import FastAPI
from routes import product, order
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="E-Commerce Backend",
    version="1.0.0"
)

# Allow requests from any origin (establish connection with frontend)...
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # specify allowed origins here
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "E-Commerce Backend API is running."}


# Product route...
app.include_router(product.router)

# Order route...
app.include_router(order.router)
