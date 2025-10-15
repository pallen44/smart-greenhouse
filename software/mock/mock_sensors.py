'''Mock sensor data publisher for greenhouse monitoring system.'''
import time
from datetime import datetime, timezone
import json
import random
from paho.mqtt.enums import CallbackAPIVersion
import paho.mqtt.client as mqtt

# MQTT broker config
BROKER = "localhost"
PORT = 1883
TOPIC_PREFIX = "greenhouse"

# Simulated sensors
def get_mock_readings():
    """Generate realistic sensor data."""
    timestamp = datetime.now(timezone.utc).isoformat()     # Timestamp
    temperature = round(random.uniform(20.0, 28.0), 1)     # °C
    temperature += random.uniform(-0.2, 0.2)               # small fluctuation
    humidity = round(random.uniform(45.0, 70.0), 1)        # %
    soil_moisture = round(random.uniform(0.3, 0.8), 2)     # 0–1 normalized
    light_intensity = random.choice([True, False])         # light on/off
    return {
        "timestamp": timestamp,
        "temperature": temperature,
        "humidity": humidity,
        "soil_moisture": soil_moisture,
        "light_on": light_intensity
    }

# Connect to broker
client = mqtt.Client(client_id="mock_sensors", callback_api_version=CallbackAPIVersion.VERSION2)
client.connect(BROKER, PORT, 60)
print(f"Connected to MQTT broker at {BROKER}:{PORT}")

try:
    while True:
        data = get_mock_readings()
        payload = json.dumps(data)
        TOPIC = f"{TOPIC_PREFIX}/readings"
        client.publish(TOPIC, payload)
        print(f"→ Published {payload} to topic '{TOPIC}'")
        time.sleep(5)  # send every 5 seconds
except KeyboardInterrupt:
    print("\nStopping publisher...")
    client.disconnect()
