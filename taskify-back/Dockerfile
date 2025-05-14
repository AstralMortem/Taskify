# Base image with Python and security updates
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.8.2

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl gcc build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry (optional, if you're using it)
RUN pip3 install poetry

# Copy dependencies
COPY pyproject.toml poetry.lock* README.md /app/

# Copy the entire app
COPY . /app


# Install Python dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

ARG RAILWAY_PUBLIC_DOMAIN
ARG RAILWAY_PRIVATE_DOMAIN
ARG RAILWAY_PROJECT_NAME
ARG RAILWAY_ENVIRONMENT_NAME
ARG RAILWAY_SERVICE_NAME
ARG RAILWAY_PROJECT_ID
ARG RAILWAY_ENVIRONMENT_ID
ARG RAILWAY_SERVICE_ID
ARG ORIGIN


ENV ORIGIN=${ORIGIN} \
  RAILWAY_PUBLIC_DOMAIN=$RAILWAY_PUBLIC_DOMAIN \
  RAILWAY_PRIVATE_DOMAIN=$RAILWAY_PRIVATE_DOMAIN \
  RAILWAY_PROJECT_NAME=$RAILWAY_PROJECT_NAME \
  RAILWAY_ENVIRONMENT_NAME=$RAILWAY_ENVIRONMENT_NAME \
  RAILWAY_SERVICE_NAME=$RAILWAY_SERVICE_NAME \
  RAILWAY_PROJECT_ID=$RAILWAY_PROJECT_ID \
  RAILWAY_ENVIRONMENT_ID=$RAILWAY_ENVIRONMENT_ID \
  RAILWAY_SERVICE_ID=$RAILWAY_SERVICE_ID

# Expose the port Railway expects
EXPOSE 8000


# Command to run the app using Uvicorn
CMD ["poetry", "run", "migration", "&&", "poetry", "run", "server"]
