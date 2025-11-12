# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gunicorn

# Copy application code
COPY backend/ ./backend/
COPY scraper/ ./scraper/
COPY .env* ./
COPY start.sh ./

# Create directory for SQLite database
RUN mkdir -p /app/data

# Make startup script executable
RUN chmod +x start.sh

# Expose port (will be overridden by $PORT in production)
EXPOSE 5001

# Run with startup script that handles dynamic port
CMD ["./start.sh"]
