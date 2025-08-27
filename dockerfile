FROM python:3.11-slim

WORKDIR /app

# rework with requirements.txt
# RUN pip install --no-cache-dir fastapi uvicorn requests
COPY requirements.txt .

RUN python -m pip install -r requirements.txt

# Copy application code
COPY . /app

# Expose port for FastAPI
EXPOSE 8000

# Default command to run the server
CMD ["uvicorn", "connector_api:app", "--host", "0.0.0.0", "--port", "8000"]
