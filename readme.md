
# E-Commerce Backend API

A backend system for an e-commerce-like product catalog and order system using **FastAPI** and **MongoDB**.

---

## Project Structure

```
ecommerce_app/
│
├── main.py               # FastAPI app entrypoint
├── database.py           # MongoDB connection setup
├── models/
│   ├── product_model.py  # Product schemas
│   └── order_model.py    # Order schemas
├── routes/
│   ├── product.py        # Product APIs
│   └── order.py          # Order APIs
├── .env                  # MongoDB URI
├── requirements.txt
```

---

## Tech Stack

- **FastAPI** - Web framework
- **MongoDB** - NoSQL Database
- **Motor** - Async MongoDB driver
- **Uvicorn** - ASGI server

---

## Setup Instructions

1. **Clone the repository**

   ```bash
   git clone https://github.com/Arpit-singh12/Ecomm_backend.git
   ```

2. **Create a virtual environment and activate it**

   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/macOS
   venv\Scripts\activate      # Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run MongoDB** (locally or via MongoDB Atlas) NOTE : If your'e using MongoDb locally then change MONGO_URI="Base MongoDb_URL"

5. **Start the FastAPI server**

   ```bash
   uvicorn app.main:app --reload
   ```

6. **Test the API using Postman or Swagger UI**

   Open browser: [http://localhost:8000/docs](http://localhost:8000/docs)

---

##  API Endpoints

###  Product APIs

#### Create Product

- **Endpoint**: `POST /products`
- **Request Body**:

```json
{
  "name": "Sample Product",
  "price": 99.99,
  "sizes": [
    {
      "size": "M",
      "quantity": 10
    }
  ]
}
```

- **Response**:

```json
{
  "id": "1234567890"
}
```

- **Status**: `201 Created`

---

#### List Products
- **Endpoint**: `GET /products?name=<Product_name>&size=<Size>&limit=5&offset=0`
- **Query Parameters**:
  - `name`: partial search
  - `size`: filter by size
  - `limit`: number of results
  - `offset`: pagination skip

- **Response**:

```json
{
  "data": [
    {
      "id": "123",
      "name": "Shirt",
      "price": 100.0
    }
  ],
  "page": {
    "next": "10",
    "limit": 10,
    "previous": 0
  }
}
```

- **Status**: `200 OK`

---

###  Order APIs

#### Create Order

- **Endpoint**: `POST /orders`
- **Request Body**:

```json
{
  "userId": "user_1",
  "items": [
    {
      "productID": "1234567890",
      "qty": 3
    },
    {
      "productID": "22222",
      "qty": 2
    }
  ]
}
```

- **Response**:

```json
{
  "id": "order_id"
}
```

- **Status**: `201 Created`

---

#### List of Orders

- **Endpoint**: `GET /orders/<user_id>?limit=2&offset=0`
- **Query Parameters**:
  - `limit`: number of documents to return
  - `offset`: pagination skip

- **Response**:

```json
{
    "data": [
        {
            "_id": "687b1fe8a426ec801fb898d9",
            "items": [
                {
                    "productDetails": {
                        "name": "Denim",
                        "ID": "687af97656fdd012aafe0472"
                    },
                    "qty": 2
                },
                {
                    "productDetails": {
                        "name": "Track-suits",
                        "ID": "687af98856fdd012aafe0473"
                    },
                    "qty": 2
                }
            ],
            "total": 1996.0
        }
    ],
    "page": {
        "next": 10,
        "previous": 0,
        "limit": 10
    }
}
```

- **Status**: `200 OK`

---


