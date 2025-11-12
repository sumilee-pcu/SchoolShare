#!/bin/bash
# Startup script for Render deployment

# Use PORT environment variable if available, otherwise default to 5001
PORT=${PORT:-5001}

echo "Checking database..."

# Always create/recreate database tables
echo "Initializing database..."
python -m backend.create_db
echo "Database initialized successfully!"

# Try to collect fresh data on startup (but don't fail if it errors)
if [ -n "$SEOUL_OPENAPI_KEY" ]; then
    echo "Starting data collection (this may take 1-2 minutes)..."
    if python -m scraper.ingest_school_facilities; then
        echo "✅ Data collection completed successfully!"
    else
        echo "⚠️  Warning: Data collection failed, but continuing to start server..."
        echo "   The API will return empty results until data is collected."
    fi
else
    echo "⚠️  Warning: SEOUL_OPENAPI_KEY not set. Skipping data collection."
    echo "   Please set SEOUL_OPENAPI_KEY environment variable in Railway dashboard."
fi

echo "Starting gunicorn on port $PORT..."

# Run gunicorn with dynamic port
gunicorn --bind "0.0.0.0:$PORT" \
         --workers 4 \
         --timeout 120 \
         --access-logfile - \
         --error-logfile - \
         backend.main:app
