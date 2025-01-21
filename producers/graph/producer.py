from kafka import KafkaProducer
import json
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    future = producer.send(TOPIC_NAME, message)
    try:
        record_metadata = future.get(timeout=10)
        logger.info(f"Producer2 sent: {message} to topic {record_metadata.topic} partition {record_metadata.partition} offset {record_metadata.offset}")
    except Exception as e:
        logger.error(f"Failed to send message: {e}")
    time.sleep(1)

producer.close()