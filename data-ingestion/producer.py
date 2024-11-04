
from kafka import KafkaProducer
import json
import time
import random
import pandas as pd




# Initialize the Kafka producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',  # Replace with your Kafka server if different
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Serialize data as JSON
)

topic_name = 'stream-topic'  # Replace with your topic name



df=pd.read_csv(f"data-ingestion/indexProcessed.csv")

try:
    while True:
        # Generate sample data
        data = {
            'timestamp': time.time(),
            'value': df.sample(1).to_dict(orient="records")[0]  # Random integer as an example
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
