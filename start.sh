#!/bin/bash
# Startup script for Render deployment

# Use PORT environment variable if available, otherwise default to 5001
PORT=${PORT:-5001}

echo "Starting gunicorn on port $PORT..."

# Run gunicorn with dynamic port
gunicorn --bind "0.0.0.0:$PORT" \
         --workers 4 \
         --timeout 120 \
         --access-logfile - \
         --error-logfile - \
         backend.main:app
