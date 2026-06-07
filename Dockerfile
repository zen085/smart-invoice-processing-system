# Python base image
FROM python:3.12-slim

# Prevent Python from buffering logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies (IMPORTANT for psycopg, Pillow, etc.)
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     libpq-dev \
#     && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create non-root user
RUN useradd -m appuser

# Change ownership (IMPORTANT)
RUN chown -R appuser:appuser /app

USER appuser

# Expose port
EXPOSE 8000

# Run Django (Gunicorn)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]