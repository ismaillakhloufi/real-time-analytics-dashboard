
from kafka import KafkaProducer
import json
import time
import random

# Initialize the Kafka producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',  # Replace with your Kafka server if different
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Serialize data as JSON
)

topic_name = 'stream-topic'  # Replace with your topic name

try:
    while True:
        # Generate sample data
        data = {
            'timestamp': time.time(),
            'value': random.randint(1, 100)  # Random integer as an example
        }
        # Send data to the Kafka topic
        producer.send(topic_name, value=data)
        print(f"Sent: {data}")
        
        # Wait for a short period before sending the next message
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopped by user")
finally:
    # Close the producer to release resources
    producer.close()
