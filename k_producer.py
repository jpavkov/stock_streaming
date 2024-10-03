from kafka import KafkaProducer
import json
import time
import requests

# Set up Kafka producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# API endpoint and key to get S&P 500 data
API_URL = "https://api.example.com/sp500"
API_KEY = "your_api_key"


def fetch_sp500_data():
    # Simulated API request to fetch S&P 500 data
    response = requests.get(API_URL, params={"apikey": API_KEY})
    if response.status_code == 200:
        return response.json()
    else:
        return None


# Stream data into Kafka every second
while True:
    data = fetch_sp500_data()
    if data:
        producer.send('sp500_data', value=data)
        print(f"Sent data to Kafka: {data}")
    time.sleep(1)
