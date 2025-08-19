#!/bin/bash

echo "Starting NetSales2B system..."

# Start database migrations
echo "Running database migrations..."
alembic upgrade head

# Start Celery worker in background
echo "Starting Celery worker..."
celery -A app.tasks.celery_app worker --loglevel=info &

# Start Celery beat scheduler in background
echo "Starting Celery beat scheduler..."
celery -A app.tasks.celery_app beat --loglevel=info &

# Start FastAPI application
echo "Starting FastAPI application..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload