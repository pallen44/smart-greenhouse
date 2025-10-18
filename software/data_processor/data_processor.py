"""Data processor that subscribes to MQTT topics and writes sensor data to InfluxDB."""
import json
import time
import os
from datetime import datetime
from typing import Any, Dict
from paho.mqtt.enums import CallbackAPIVersion
import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point

# MQTT Configuration
MQTT_BROKER = os.getenv("MQTT_BROKER", "mosquitto")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_TOPIC = "greenhouse/readings"

# InfluxDB Configuration
INFLUXDB_URL = os.getenv("INFLUXDB_URL", "http://influxdb:8086")
INFLUXDB_TOKEN = os.getenv("INFLUXDB_TOKEN", "")
INFLUXDB_ORG = os.getenv("INFLUXDB_ORG", "greenhouse")
INFLUXDB_BUCKET = os.getenv("INFLUXDB_BUCKET", "sensor_data")

# Initialize InfluxDB client and write API
influx_client = InfluxDBClient(
    url=INFLUXDB_URL,
    token=INFLUXDB_TOKEN,
    org=INFLUXDB_ORG
)
write_api = influx_client.write_api()


def write_to_influx(data: Dict[str, Any]) -> None:
    """
    Write a dictionary of sensor data to InfluxDB.
    """
    try:
        point = (
            Point("greenhouse_env")
            .tag("sensor_id", data.get("sensor_id", "default_sensor"))
            .tag("zone", data.get("zone", "default_zone"))
            .tag("plant", data.get("plant", "default_plant"))
            .field("air_temp_c", float(data["air_temp_c"]))
            .field("rel_humidity", float(data["rel_humidity"]))
            .field("soil_moisture", float(data["soil_moisture"]))
            .field("water_tank_level", float(data.get("water_tank_level", 0.0)))
            .field("light_on", int(data.get("light_on", 0)))
            .field("fan_on", int(data.get("fan_on", 0)))
            .field("pump_on", int(data.get("pump_on", 0)))
            .time(datetime.fromisoformat(data["timestamp"]))
        )
        write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)
        print(f"✔ Written to InfluxDB at {data['timestamp']}")
    except Exception as exc:  # pylint: disable=broad-except
        print(f"! Failed to write to InfluxDB: {exc}")


def on_message(_client: mqtt.Client, _userdata: Any, msg: mqtt.MQTTMessage) -> None:
    """
    Handle incoming MQTT messages.

    Args:
        _client: MQTT client instance.
        _userdata: Optional user data (not used).
        msg: The MQTT message object containing topic and payload.
    """
    try:
        payload = msg.payload.decode("utf-8")
        data = json.loads(payload)

        required_keys = {"air_temp_c", "rel_humidity", "soil_moisture", "light_on", "timestamp"}
        if not required_keys.issubset(data.keys()):
            print("! Invalid data format: missing required keys.")

        write_to_influx(data)
    except json.JSONDecodeError:
        print("! Invalid JSON payload received.")
    except (ValueError, KeyError, TypeError) as exc:
        print(f"! Error handling message: {exc}")


def on_connect(client: mqtt.Client, _userdata: Any, _flags: Dict[str, Any],
               rc: int, _properties: Any = None) -> None:
    """
    Handle MQTT broker connection event.

    Args:
        client: MQTT client instance.
        _userdata: Optional user data (not used).
        _flags: Response flags sent by the broker.
        rc: Connection result code (0 = success).
        _properties: MQTT v5 properties (not used for v3 clients).
    """
    if rc == 0:
        print("Connected to MQTT broker.")
        client.subscribe(MQTT_TOPIC)
        print(f"📡 Subscribed to topic '{MQTT_TOPIC}'")
    else:
        print(f"! Failed to connect to MQTT broker, return code {rc}")


def main() -> None:
    """
    Main entry point for the data processor.

    Initializes the MQTT client, connects to the broker, subscribes to the
    configured topic, and keeps the process running until interrupted.
    """
    print(f"Connecting to MQTT broker at {MQTT_BROKER}:{MQTT_PORT} ...")

    client = mqtt.Client(
        client_id="data_processor",
        callback_api_version=CallbackAPIVersion.VERSION2
    )
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect_async(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()

    print("Listening for messages...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping data processor...")
    finally:
        client.loop_stop()
        client.disconnect()
        influx_client.close()
        print("Disconnected cleanly.")


if __name__ == "__main__":
    main()
