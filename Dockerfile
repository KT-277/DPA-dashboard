# Use official Python base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your Python script into the container
COPY otx_ingest.py .

# Set the default command to run the script
CMD ["python", "otx_ingest.py"]
