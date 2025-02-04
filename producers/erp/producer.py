import os
from kafka import KafkaProducer
import pymysql
import json
import time
from decimal import Decimal

# Custom JSON encoder
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)  # or float(obj)
        return super(CustomJSONEncoder, self).default(obj)

# Get environment variables
KAFKA_BROKER = os.getenv('KAFKA_ADVERTISED_LISTENERS', 'kafka:9092')
MYSQL_HOST = os.getenv('MYSQL_HOST', 'mysql')
MYSQL_USER = os.getenv('MYSQL_USER', 'clothes')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'clothes')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'clothes')

# Kafka connection
TOPIC_NAME = 'clothes-topic'
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    api_version=(0, 10, 1),
    value_serializer=lambda v: json.dumps(v, cls=CustomJSONEncoder).encode('utf-8')
)

# MySQL connection
connection = pymysql.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=MYSQL_DATABASE
)

try:
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        # Read from DB
        sql = "SELECT * FROM CLOTHES"
        cursor.execute(sql)
        result = cursor.fetchall()

        # Push to Kafka
        index = 0
        for row in result:
            producer.send(TOPIC_NAME, row)
            index += 1
            if index % 10 == 0:
                producer.flush()
                time.sleep(10)  # Sleep for 10 seconds
finally:
    connection.close()
    producer.close()
