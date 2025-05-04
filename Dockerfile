FROM python:3.12-slim

# Install system dependencies required for face_recognition (dlib)
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libglib2.0-0 \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directory for environment variables
RUN mkdir -p assets/env

# Expose port
EXPOSE 8080

# Command to run the application
CMD ["python", "main.py"]
