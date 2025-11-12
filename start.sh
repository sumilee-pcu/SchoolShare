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

    # Populate data in background to not delay server startup
    if [ -n "$SEOUL_OPENAPI_KEY" ]; then
        echo "Starting background data collection..."
        nohup bash -c "sleep 5 && python -m scraper.ingest_school_facilities && echo 'Data collection completed!'" > data_collection.log 2>&1 &
        echo "Data collection started in background. Check data_collection.log for progress."
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
