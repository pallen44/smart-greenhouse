# Use a lightweight Python base image
FROM python:3.11-slim

# Create and switch to /app
WORKDIR /app

# Copy everything from this folder into the container
COPY . .

# Install dependencies
# This service needs only MQTT
RUN pip install --no-cache-dir paho-mqtt

# The environment variables (e.g., MQTT_BROKER) are injected
# from docker-compose via the .env file

# Start the mock sensor publisher
CMD ["python", "-u", "mock_sensors.py"]
