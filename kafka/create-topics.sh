#!/bin/bash
# Start Kafka
/bin/bash /etc/confluent/docker/run &

# Wait for Kafka to start
while ! nc -z localhost 9092; do
  sleep 1
done

# Create topics
kafka-topics --create --topic clothes-topic --partitions 1 --replication-factor 1 --bootstrap-server localhost:9092
kafka-topics --create --topic users-topic --partitions 1 --replication-factor 1 --bootstrap-server localhost:9092

# Keep the container running
tail -f /dev/null
