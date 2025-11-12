#!/bin/bash
# Startup script for Render deployment

# Use PORT environment variable if available, otherwise default to 5001
PORT=${PORT:-5001}

echo "Checking database..."

# Check if database exists, if not create it
if [ ! -f "schoolshare.db" ]; then
    echo "Database not found. Creating database..."
    python -m backend.create_db
    echo "Database created successfully!"

    # Populate data immediately before starting server (only on first run)
    if [ -n "$SEOUL_OPENAPI_KEY" ]; then
        echo "Collecting school facility data (this may take 1-2 minutes)..."
        python -m scraper.ingest_school_facilities
        echo "✅ Data collection completed!"
    else
        echo "Warning: SEOUL_OPENAPI_KEY not set. Skipping data collection."
    fi
else
    echo "Database already exists. Skipping initialization."
fi

echo "Starting gunicorn on port $PORT..."

# Run gunicorn with dynamic port
gunicorn --bind "0.0.0.0:$PORT" \
         --workers 4 \
         --timeout 120 \
         --access-logfile - \
         --error-logfile - \
         backend.main:app
