# Use official Python image
FROM python:3.10-slim

# Install system dependencies + pipenv
RUN apt-get update && apt-get install -y build-essential && pip install pipenv

# Set working directory
WORKDIR /app

# Copy Pipenv files first (for Docker caching)
COPY Pipfile Pipfile.lock ./

# Install Python packages inside Pipenv environment
RUN pipenv install --deploy --ignore-pipfile

# Copy rest of the application
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Start FastAPI using Uvicorn via Pipenv
CMD ["pipenv", "run", "uvicorn", "app_api:app", "--host", "0.0.0.0", "--port", "8000"]
