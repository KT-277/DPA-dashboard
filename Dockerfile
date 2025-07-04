# Use official Python base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your FastAPI script and model file
COPY predict_service.py .
COPY anomaly_model.pkl .

# Expose port 8000
EXPOSE 8000

# Run FastAPI app with Uvicorn
CMD ["uvicorn", "predict_service:app", "--host", "0.0.0.0", "--port", "8000"]

