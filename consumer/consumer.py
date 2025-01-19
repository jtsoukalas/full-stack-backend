from kafka import KafkaConsumer
import json

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

for message in consumer:
    print(f"Received message from topic {message.topic}: {message.value}")