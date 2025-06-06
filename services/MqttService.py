import json
import asyncio
import os
import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion
from dotenv import load_dotenv
from services.FrequencyService import ROCOFCalculator

# Load environment variables
load_dotenv()

# MQTT Configuration from .env
MQTT_USER = os.getenv("MQTT_AWS_USER")
MQTT_PASS = os.getenv("MQTT_AWS_PASS")
MQTT_HOST = os.getenv("MQTT_AWS_HOST").replace("mqtt://", "")  # Remove 'mqtt://' prefix
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))  # Default to 1883 if not set
CLIENT_ID = os.getenv("AWS_CLIENT_ID")

# Queue to hold incoming MQTT data before processing
mqtt_queue = asyncio.Queue()
rocofCalculator = ROCOFCalculator(window_size=900, sampling_interval=2.0)

def normalize_payload(payload: dict) -> dict:
    result = {}
    # print("payload")
    # print(payload.items())
    # Lowercase top-level keys except 'units' or 'lines'
    for key, value in payload.items():
        if key not in ['units', 'lines', 'transformers']:
            result[key.lower()] = value

    # Use 'units' or 'lines' as components
    raw_components = payload.get("units") or payload.get("lines") or payload.get("transformers") or payload.get("units") or []

    components = []
    # print("raw components")
    # print(raw_components)
    for comp in raw_components:
        # if not isinstance(comp, dict):
        #     continue

        comp_id = comp.get("id", "").lower()
        data = {}

        # Find the first key that is not 'id' (e.g., 'gd', 'td', 'pd')
        nested_key = next((k for k in comp if k != "id"), None)
        if nested_key:
            # print("comp")
            # print(comp[nested_key])
            # if isinstance(comp[nested_key], dict):
            for k, v in comp[nested_key].items():
                data[k.lower()] = v
            # else:
            #     data[nested_key.lower()] = comp[nested_key]

        components.append({
            "id": comp_id,
            "data": data
        })

    result["components"] = components
    return result


# Start the MQTT client
def start_mqtt(loop: asyncio.AbstractEventLoop):
    # ✅ Explicitly set the callback API version
    client = mqtt.Client(client_id=CLIENT_ID, callback_api_version=CallbackAPIVersion.VERSION1)

    # client = mqtt.Client(CLIENT_ID)  # Use client ID from .env
    client.username_pw_set(MQTT_USER, MQTT_PASS)  # Set credentials

    # This function is triggered when an MQTT message is received
    def on_message(client, userdata, msg):
        # print("message")
        try:
            # Decode payload from bytes to JSON
            payload = json.loads(msg.payload.decode())
            # print('mqtt')
            # print(payload)

            # Normalize the payload
            normalized = normalize_payload(payload)

            # print(normalized)
            rocofCalculator.process_frequency_data(normalized)

            # Safely push the data to the async queue using asyncio thread-safe method
            asyncio.run_coroutine_threadsafe(mqtt_queue.put(normalized), loop)
        except UnicodeDecodeError as e:
            print(f"[Decode Error] Topic: {msg.topic} - Could not decode message: {e}")
        except json.JSONDecodeError as e:
            print(f"[JSON Error] Topic: {msg.topic} - Invalid JSON: {e}")
        except Exception as e:
            print(f"[Unknown Error] Topic: {msg.topic} - {e}")

    client.on_message = on_message # Set callback for incoming messages

    # Connect to broker (extracted from .env)
    client.connect(MQTT_HOST, MQTT_PORT, 60)

    topics = [
        ("odukpanits/tv", 0),  # QoS 0
        ("kainjits/tv", 0),  # QoS 1
        ("ndphc/phoenix/ogun/pd", 0),
        ("odukpanits/tv", 0),
        ("phmains/tv", 1),
        # ("transamadi/tv", 0)
        # ("power-grid/alerts", 2),  # QoS 2
    ]

    # Subscribe to all topics at once
    client.subscribe(topics)
    # client.subscribe("power-grid/stations")  # Subscribe to the topic
    client.loop_start()  # Start MQTT listener loop in a non-blocking way
