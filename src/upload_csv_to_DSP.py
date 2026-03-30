

import requests
import csv
from confluent_kafka import Producer
from confluent_kafka.serialization import StringSerializer, SerializationContext, MessageField
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
import time
import os
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file


API_GATEWAY_URL = os.getenv("API_GATEWAY_URL", "")
API_GATEWAY_TOKEN = os.getenv("API_GATEWAY_TOKEN", "")
    
# --- Configuration ---
API_URL = f"{API_GATEWAY_URL}/api/v1/upload"
STATUS_URL = f"{API_GATEWAY_URL}/api/v1/status/"

SORTED_DF_CSV_PATH = "raw_data/subs_info_data.csv"

# Explicitly bypass your corporate proxy for local testing
PROXIES = {
    "http": None,
    "https": None,
}

HEADERS = {
    "X-API-Key": API_GATEWAY_TOKEN
}


def upload_via_api_gateway(SORTED_DF_CSV_PATH, KAFKA_TOPIC):
    """Uploads the file and polls for the result."""

    # 1. Define the metadata for the form
    payload = {
        "source_system": KAFKA_TOPIC,
        "kafka_topic": KAFKA_TOPIC,
        "rec_id_col": "rec_id"
    }

    # 2. Open the file and send the POST request
    print(f"\nSending POST request to {API_URL}...")
    with open(SORTED_DF_CSV_PATH, 'rb') as f:
        files = {
            'file': (SORTED_DF_CSV_PATH, f, 'text/csv')
        }

        response = requests.post(
            API_URL,
            data=payload,
            files=files,
            headers=HEADERS,
            proxies=PROXIES 
        )

    if response.status_code != 200:
        print(f"Upload Failed: {response.status_code}")
        print(response.text)
        return

    # 3. Parse the Job ID from the response
    result = response.json()
    print("Upload Successful! Server Response:")
    print(result)

    job_id = result.get("job_id")
    if not job_id:
        return

    # 4. Poll the status endpoint until the background job finishes
    print(f"\nPolling status for Job ID: {job_id}...")
    while True:
        status_response = requests.get(f"{STATUS_URL}{job_id}",
                                       headers=HEADERS,
                                       proxies=PROXIES
                                       )

        if status_response.status_code == 200:
            status_data = status_response.json()
            current_status = status_data.get("status")

            if current_status == "processing":
                print("Still processing... waiting 5 seconds.")
                time.sleep(5)
            else:
                print("\nFinal Job Status:")
                print(status_data)
                break
        else:
            print(f"Failed to check status: {status_response.status_code}")
            break


if __name__ == "__main__":

    SORTED_DF_CSV_PATH = "raw_data/subs_info_data.csv"
    KAFKA_TOPIC = os.getenv("KAFKA_TOPIC") #"xxx_daily_dsp"
    
    upload_via_api_gateway(SORTED_DF_CSV_PATH, KAFKA_TOPIC)
