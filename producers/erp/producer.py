from kafka import KafkaProducer
import json
import time

KAFKA_BROKER = 'kafka:9092'
TOPIC_NAME = 'clothes-topic'

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    api_version=(0, 10, 1),
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

for i in range(5):
    message = {"producer": "Producer1", "message": f"Hello from Producer1 {i}"}
    producer.send(TOPIC_NAME, message)
    print(f"Producer1 sent: {message}")
    time.sleep(1)

producer.close()
