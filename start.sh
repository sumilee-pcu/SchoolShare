#!/bin/bash
# Startup script for Render deployment

# Use PORT environment variable if available, otherwise default to 5001
PORT=${PORT:-5001}

echo "Checking database..."

# Check if database exists, if not create it and populate with data
if [ ! -f "schoolshare.db" ]; then
    echo "Database not found. Creating and populating database..."
    python -m backend.create_db

    # Only populate data if API key is set
    if [ -n "$SEOUL_OPENAPI_KEY" ]; then
        echo "Collecting school facility data..."
        python -m scraper.ingest_school_facilities
        echo "Data collection completed!"
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
