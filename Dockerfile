# Use the official lightweight Python 3.13 image
FROM python:3.13-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the dependencies file and install them safely
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your FastAPI application code
COPY main.py .

# Expose port 8443 for secure Kubernetes webhook traffic
EXPOSE 8443

# Run Uvicorn on port 8443 and instruct it to use TLS certificates
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8443", "--ssl-keyfile", "/certs/tls.key", "--ssl-certfile", "/certs/tls.crt"]
