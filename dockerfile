FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

COPY . /app

EXPOSE 8000

CMD ["uvicorn", "connector_api:app", "--host", "0.0.0.0", "--port", "8000"]
