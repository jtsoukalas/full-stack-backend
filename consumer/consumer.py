import os
from kafka import KafkaConsumer
from pymongo import MongoClient
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get environment variables
KAFKA_BROKER = os.getenv('KAFKA_ADVERTISED_LISTENERS', 'kafka:9092')

# Kafka connection
KAFKA_TOPICS = ['users-topic', 'clothes-topic']
consumer = KafkaConsumer(
    *KAFKA_TOPICS,
    bootstrap_servers=KAFKA_BROKER,
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group',
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

# MongoDB connection
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://mongodb:27017')
client = MongoClient(MONGO_URI)
db = client['db']
collection_users = db['users']
collection_clothes = db['clothes']


for message in consumer:
    topic = message.topic
    data = message.value
    logger.info(data)

    if topic == 'users-topic':
        user_id = data.get('node', {}).get('userId')
        outgoing_relations = data.get('outgoing_relations', [])

        if user_id:
            logger.info(f"Processing user {user_id}")
            logger.info(f"with outgoing relations {outgoing_relations}")

            # Update only non-array fields with $set
            filtered_data = {k: v for k, v in data.items() if k != 'outgoing_relations'}

            # Ensure data update
            collection_users.update_one(
                {'node.userId': user_id},
                {'$set': filtered_data},
                upsert=True
            )

            # Always update outgoing_relations
            for relation in outgoing_relations:
                collection_users.update_one(
                    {'node.userId': user_id},
                    {'$addToSet': {'outgoing_relations': relation}}
                )
    elif topic == 'clothes-topic':
        clothes_id = data.get('clothID')
        if clothes_id:
            collection_clothes.update_one(
                {'clothesID': clothes_id},
                {'$set': data},
                upsert=True
            )