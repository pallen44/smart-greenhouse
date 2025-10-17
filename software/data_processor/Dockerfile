# Base Python image
FROM python:3.11-slim

# Work directory
WORKDIR /app

# Copy current folder into container
COPY . .

# Install dependencies
# This service needs both MQTT and InfluxDB client libraries
RUN pip install --no-cache-dir paho-mqtt influxdb-client

# Environment variables (INFLUXDB_URL, TOKEN, etc.)
# are automatically passed from docker-compose .env file

# Start the processor
CMD ["python", "-u", "data_processor.py"]
