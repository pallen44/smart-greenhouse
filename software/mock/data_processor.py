'''Data processor that subscribes to MQTT topics and writes sensor data to InfluxDB.'''
import json
from datetime import datetime
from paho.mqtt.enums import CallbackAPIVersion
import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point

# MQTT Configuration
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "greenhouse/readings"

# InfluxDB Configuration
INFLUXDB_URL = "http://localhost:8086"
INFLUXDB_TOKEN = "WXLfMiThi8oJcu0dx3Z6uQDE-D02O6C8Ssvqpc5zLY" \
"BfoDlkAPpXrQvr1WVrDt4O4sQHhDAMYzrxsFNz2jYMlw=="
INFLUXDB_ORG = "greenhouse"
INFLUXDB_BUCKET = "sensor_data"

# Setup InfluxDB client
influx_client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
write_api = influx_client.write_api()

# Function to write incoming data to InfluxDB
def write_to_influx(data):
    """Write a dictionary of sensor data to InfluxDB."""
    try:
        point = (
            Point("sensor_readings")
            .tag("location", "greenhouse")
            .field("temperature", float(data["temperature"]))
            .field("humidity", float(data["humidity"]))
            .field("soil_moisture", float(data["soil_moisture"]))
            .field("light_on", int(data["light_on"]))
            .time(datetime.fromisoformat(data["timestamp"]))
        )
        write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)
    except Exception as e: # pylint: disable=broad-except
        print(f"! Failed to write to InfluxDB: {e}")

# MQTT Callback
def on_message(_client, _userdata, msg):
    """Handle new MQTT messages."""
    try:
        payload = msg.payload.decode("utf-8")
        data = json.loads(payload)

        required_keys = {"temperature", "humidity", "soil_moisture", "light_on"}
        if not required_keys.issubset(data.keys()):
            print("! Invalid data format, missing keys.")
            return

        write_to_influx(data)

    except json.JSONDecodeError:
        print("! Invalid JSON payload received")
    except (ValueError, KeyError, TypeError) as e:
        print(f"! Error handling message: {e}")

# Main execution loop
if __name__ == "__main__":
    print(f"Connecting to MQTT broker at {MQTT_BROKER}:{MQTT_PORT} ...")
    client = mqtt.Client(client_id="data_processor", callback_api_version=CallbackAPIVersion.VERSION2)
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.subscribe(MQTT_TOPIC)
    print(f"Listening for messages on topic '{MQTT_TOPIC}'...")

    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("Stopping data processor...")
    finally:
        client.disconnect()
        influx_client.close()
        print("Disconnected cleanly.")
