FROM python:3.12-slim

WORKDIR /code

# Install dependencies first for better layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and the pre-trained model
COPY app/ ./app/
COPY model/ ./model/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
