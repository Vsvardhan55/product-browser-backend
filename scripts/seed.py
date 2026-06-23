from faker import Faker
from datetime import datetime, timedelta
from random import choice, uniform
from app.database import SessionLocal
from app.models import Product

fake = Faker()

categories = [
    "Electronics",
    "Books",
    "Fashion",
    "Sports",
    "Home",
    "Beauty",
    "Toys"
]

BATCH_SIZE = 10000
TOTAL_PRODUCTS = 200000

db = SessionLocal()

for batch_start in range(0, TOTAL_PRODUCTS, BATCH_SIZE):

    products = []

    for _ in range(BATCH_SIZE):

        created = fake.date_time_between(
            start_date="-2y",
            end_date="now"
        )

        updated = created + timedelta(
            days=fake.random_int(0, 100)
        )

        products.append(
            Product(
                name=fake.word().title(),
                category=choice(categories),
                price=round(uniform(10, 1000), 2),
                created_at=created,
                updated_at=updated
            )
        )

    db.bulk_save_objects(products)
    db.commit()

    print(
        f"Inserted {batch_start + BATCH_SIZE} products"
    )

db.close()

print("Finished seeding 200000 products")