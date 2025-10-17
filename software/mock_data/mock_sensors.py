'''Mock sensor data publisher for greenhouse monitoring system.'''
import time
from datetime import datetime, timezone
import json
import os
import random
from paho.mqtt.enums import CallbackAPIVersion
import paho.mqtt.client as mqtt

# MQTT broker config
BROKER = os.getenv("MQTT_BROKER", "mosquitto")
PORT = int(os.getenv("MQTT_PORT", "1883"))
TOPIC_PREFIX = "greenhouse"

# Simulated sensors
def get_mock_readings():
    """Generate realistic sensor data."""
    timestamp = datetime.now(timezone.utc).isoformat()     # Timestamp
    temperature = round(random.uniform(20.0, 28.0), 1)     # °C
    temperature += random.uniform(-0.2, 0.2)               # small fluctuation
    humidity = round(random.uniform(45.0, 70.0), 1)        # %
    soil_moisture = round(random.uniform(0.3, 0.8), 2)     # 0–1 normalized
    light_on = random.choice([True, False])                # light on/off
    fan_on = random.choice([True, False])                  # fan on/off
    pump_on = random.choice([True, False])                 # pump on/off
    water_tank_level = round(random.uniform(0.1, 1.0), 2)  # 0–1 normalized
    return {
        "timestamp": timestamp,
        "air_temp_c": temperature,
        "rel_humidity": humidity,
        "soil_moisture": soil_moisture,
        "light_on": light_on,
        "fan_on": fan_on,
        "pump_on": pump_on,
        "water_tank_level": water_tank_level,
        "sensor_id": "esp32-1",
        "zone": "fake_zone",
        "plant": "fake_plant"
    }


# Connect to broker
client = mqtt.Client(client_id="mock_sensors", callback_api_version=CallbackAPIVersion.VERSION2)
for attempt in range(10):
    try:
        client.connect(BROKER, PORT, 60)
        print(f"Connected to MQTT broker at {BROKER}:{PORT}")
        break
    except Exception as e: # pylint: disable=broad-except
        print(f"MQTT connection failed (attempt {attempt + 1}/10): {e}")
        time.sleep(3)
else:
    print("Could not connect to MQTT broker after 10 attempts.")
    exit(1)

# Publish mock data every 5 secondss
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
