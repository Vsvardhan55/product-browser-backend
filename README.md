# Product Browser Backend

A FastAPI + PostgreSQL backend that supports browsing 200,000 products with fast cursor pagination.

## Features

- Product listing
- Category filtering
- Cursor based pagination
- Snapshot based consistency
- PostgreSQL indexing
- Bulk data generation

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy

## Setup

Clone repository

Install dependencies:

pip install -r requirements.txt


Create .env:

DATABASE_URL=your_database_url


Run backend:

uvicorn app.main:app --reload


## Seed Database

Generate 200,000 products:

python -m scripts.seed


## API

Get products:

GET /products


Filter:

GET /products?category=Electronics


Pagination:

GET /products?cursor_time=...&cursor_id=...&snapshot_time=...


## Design Decisions

Cursor pagination is used instead of OFFSET because OFFSET becomes slow on large datasets.

The cursor uses:

(updated_at, id)

to guarantee stable ordering.

Snapshot time prevents missing or duplicate products when data changes while browsing.