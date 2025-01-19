from kafka import KafkaProducer
import json
import time

KAFKA_BROKER = 'kafka:9092'
TOPIC_NAME = 'users-topic'

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    api_version=(0, 10, 1),
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    request_timeout_ms=60000,  # Increase request timeout to 60 seconds
    metadata_max_age_ms=60000  # Increase metadata max age to 60 seconds
)

for i in range(5):
    message = {"producer": "Producer2", "message": f"Hello from Producer2 {i}"}
    producer.send(TOPIC_NAME, message)
    print(f"Producer2 sent: {message}")
    time.sleep(1)

producer.close()
