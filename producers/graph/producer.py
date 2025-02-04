import os
from kafka import KafkaProducer
from neo4j import GraphDatabase
import json
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get environment variables
KAFKA_BROKER = os.getenv('KAFKA_ADVERTISED_LISTENERS', 'kafka:9092')
NEO4J_USER, NEO4J_PASSWORD = os.getenv('NEO4J_AUTH', 'neo4j/password').split('/')

# Kafka connection
TOPIC_NAME = 'users-topic'
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    api_version=(0, 10, 1),
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    request_timeout_ms=60000,  # Increase request timeout to 60 seconds
    metadata_max_age_ms=60000  # Increase metadata max age to 60 seconds
)

# Neo4j connection
NEO4J_URI = 'bolt://neo4j:7687'
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))


def fetch_and_send_data():
    with driver.session() as session:
        result = session.run("""
                MATCH (n:User)-[r]->(m)
                RETURN n, collect(r) as relations, collect(m) as related_nodes
            """)
        index = 0
        for record in result:
            node = record["n"]
            relations = record["relations"]
            related_nodes = record["related_nodes"]
            outgoing_relations = [
                {
                    "userId": related_node["userId"],
                    "relationship": relationship.type
                }
                for related_node, relationship in zip(related_nodes, relations)
            ]
            node_data = {
                "node": dict(node),
                "outgoing_relations": outgoing_relations
            }
            producer.send(TOPIC_NAME, node_data)
            index += 1
            if index % 5 == 0:  # Every 5 results
                producer.flush()
                time.sleep(20)  # Sleep for 20 seconds


try:
    fetch_and_send_data()
finally:
    producer.flush()
    producer.close()
    driver.close()
