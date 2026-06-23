from fastapi import FastAPI, Query
from sqlalchemy import desc
from datetime import datetime

from app.database import SessionLocal
from app.models import Product


app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {
        "message": "Product Browser Backend Running"
    }


@app.get("/products")
def get_products(
    category: str = None,
    limit: int = Query(default=20, le=100),
    cursor_time: str = None,
    cursor_id: int = None,
    snapshot_time: str = None
):

    db = SessionLocal()


    # Create snapshot for first request
    if snapshot_time is None:
        snapshot = datetime.utcnow()

    else:
        snapshot = datetime.fromisoformat(snapshot_time)


    query = db.query(Product)


    # Freeze data view
    query = query.filter(
        Product.updated_at <= snapshot
    )


    # Category filter
    if category:

        query = query.filter(
            Product.category == category
        )


    # Cursor logic

    if cursor_time and cursor_id:

        cursor_datetime = datetime.fromisoformat(
            cursor_time
        )

        query = query.filter(
            (
                Product.updated_at < cursor_datetime
            )
            |
            (
                (Product.updated_at == cursor_datetime)
                &
                (Product.id < cursor_id)
            )
        )


    products = (
        query
        .order_by(
            desc(Product.updated_at),
            desc(Product.id)
        )
        .limit(limit)
        .all()
    )


    data = []

    for p in products:

        data.append(
            {
                "id": p.id,
                "name": p.name,
                "category": p.category,
                "price": float(p.price),
                "updated_at": p.updated_at
            }
        )


    db.close()


    next_cursor = None


    if products:

        last = products[-1]

        next_cursor = {
            "cursor_time":
                last.updated_at.isoformat(),

            "cursor_id":
                last.id,

            "snapshot_time":
                snapshot.replace(microsecond=0).isoformat()
        }


    return {
        "data": data,
        "next_cursor": next_cursor
    }