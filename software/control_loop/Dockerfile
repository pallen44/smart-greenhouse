FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir paho-mqtt influxdb-client
CMD ["python", "control_loop.py"]
