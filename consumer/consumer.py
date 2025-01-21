from kafka import KafkaConsumer
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

KAFKA_BROKER = 'kafka:9092'
TOPICS = ['users-topic', 'clothes-topic']

consumer = KafkaConsumer(
    *TOPICS,
    bootstrap_servers=KAFKA_BROKER,
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group',
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

logger.info("Consumer started and subscribed to topics: %s", TOPICS)

for message in consumer:
    logger.info(f"{message.topic}: {message.value}")