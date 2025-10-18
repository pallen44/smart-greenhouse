'''Control Loop for Greenhouse Irrigation System'''
import os
import time
import json
from datetime import datetime, timezone
from paho.mqtt.enums import CallbackAPIVersion
from paho.mqtt import client as mqtt
from influxdb_client import InfluxDBClient

# --- Configuration ---
MQTT_BROKER = os.getenv("MQTT_BROKER", "mosquitto")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_CONTROL_TOPIC = "greenhouse/control"

INFLUXDB_URL = os.getenv("INFLUXDB_URL", "http://influxdb:8086")
INFLUXDB_TOKEN = os.getenv("INFLUXDB_TOKEN", "")
INFLUXDB_ORG = os.getenv("INFLUXDB_ORG", "greenhouse")
INFLUXDB_BUCKET = os.getenv("INFLUXDB_BUCKET", "sensor_data")

SOIL_MOISTURE_LOW = 0.35
SOIL_MOISTURE_HIGH = 0.45

# --- Connect to Influx ---
client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
query_api = client.query_api()

# --- Connect to MQTT ---
mqtt_client = mqtt.Client(client_id="control_loop", callback_api_version=CallbackAPIVersion.VERSION2)
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.loop_start()

def get_latest_soil_moisture():
    """Query the latest soil moisture value from InfluxDB."""
    flux_query = f'''
    from(bucket:"{INFLUXDB_BUCKET}")
      |> range(start: -5m)
      |> filter(fn: (r) => r._measurement == "greenhouse_env" and r._field == "soil_moisture")
      |> last()
    '''
    tables = query_api.query(flux_query)
    for table in tables:
        for record in table.records:
            return record.get_value()
    return None

def decide_and_publish():
    """Decide pump state and publish to MQTT."""
    value = get_latest_soil_moisture()
    if value is None:
        print("No soil moisture data found.")
        return

    print(f"Soil moisture: {value:.2f}")
    if value < SOIL_MOISTURE_LOW:
        command = {"pump_on": True, "timestamp": datetime.now(timezone.utc).isoformat()}
    elif value > SOIL_MOISTURE_HIGH:
        command = {"pump_on": False, "timestamp": datetime.now(timezone.utc).isoformat()}
    else:
        return  # within normal range, no action

    mqtt_client.publish(MQTT_CONTROL_TOPIC, json.dumps(command))
    print(f"Published control command: {command}")

if __name__ == "__main__":
    print("Control loop running...")
    try:
        while True:
            decide_and_publish()
            time.sleep(10)  # check every 10 s
    except KeyboardInterrupt:
        print("Stopping control loop...")
    finally:
        mqtt_client.loop_stop()
        mqtt_client.disconnect()
        client.close()
