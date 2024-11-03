from kafka import KafkaConsumer
import json
import time

# Initialize the Kafka consumer
consumer = KafkaConsumer(
    'stream-topic',  # Replace with your topic name
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',  # Start from the beginning if no offset is stored
    enable_auto_commit=True,
    group_id="new-group-id",  # Unique group ID
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("Listening for messages...")

while True:
    # Poll for messages (fetch data every 1 second)
    messages = consumer.poll(timeout_ms=1000)
    
    # Check if messages exist in the response
    for topic_partition, msgs in messages.items():
        for message in msgs:
            print(f"Received: {message.value}")

    time.sleep(1)  # Avoid over-polling
