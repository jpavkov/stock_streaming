from kafka import KafkaConsumer
import json
import numpy as np

# Set up Kafka consumer
consumer = KafkaConsumer(
    'sp500_data',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

# Store historical price data
price_history = []

# Function to check if a new channel is forming


def detect_channel(prices):
    if len(prices) < 10:
        return False
    highs = [data['high'] for data in prices]
    lows = [data['low'] for data in prices]

    upper_channel = np.polyfit(range(len(highs)), highs, 1)
    lower_channel = np.polyfit(range(len(lows)), lows, 1)

    # Check if the two trend lines are roughly parallel
    if abs(upper_channel[0] - lower_channel[0]) < 0.01:
        print("New channel detected!")
        return True
    return False


# Analyze incoming data in real-time
for message in consumer:
    data = message.value
    print(f"Received data: {data}")

    price_history.append(data)

    # Keep a fixed window of recent price data
    if len(price_history) > 100:
        price_history.pop(0)

    # Detect channels in the price history
    if detect_channel(price_history):
        print("Potential new trend channel detected!")
