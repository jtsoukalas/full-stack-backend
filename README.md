# Full-Stack Backend

## Overview

This project is a full-stack backend application that integrates MySQL, Neo4j, MongoDB, Kafka, and Python-based producers and consumers. 

## Prerequisites

- Docker
- Docker Compose

## Services

- **MySQL**: Stores relational data.
- **Neo4j**: Stores graph data.
- **Kafka**: Message broker for data streaming.
- **MongoDB**: Stores document data.
- **Producers**: Python scripts that read data from MySQL and Neo4j and send it to Kafka.
- **Consumer**: Python script that processes data from Kafka topics.

## Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/jtsoukalas/full-stack-backend.git
    cd full-stack-backend
    ```

   2. Create a `.env` file with the following environment variables (default values are shown):
       ```env
       MYSQL_ROOT_PASSWORD=root
       MYSQL_DATABASE=clothes
       MYSQL_USER=clothes
       MYSQL_PASSWORD=clothes
       NEO4J_AUTH=neo4j/password
       KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://kafka:9092
       MONGO_URI=mongodb://mongo:27017/
       ```

3. Start the services using Docker Compose:
    ```sh
    docker-compose up -d
    ```

## Usage

- **MySQL**: Access the MySQL database at `localhost:3307`.
- **Neo4j**: Access the Neo4j database at `localhost:7474`.
- **Kafka**: Kafka broker is available at `localhost:9092`.
- **MongoDB**: Access the MongoDB database at `localhost:27017`.

## Producers

- **ERP Producer**: Reads data from MySQL and sends it to Kafka.
- **Graph Producer**: Reads data from Neo4j and sends it to Kafka.

## Consumer

- **Kafka Consumer**: Processes data from Kafka topics.

## File Structure

- `docker-compose.yml`: Docker Compose configuration file.
- `data/`: Contains initial data for MySQL and Neo4j.
- `producers/`: Contains producer scripts.
- `consumer/`: Contains consumer scripts.
- `flask/`: Contains a Flask application that serves as an API for the data.

## Running Producers and Consumer

1. **ERP Producer**:
    ```sh
    docker-compose run erp_producer
    ```

2. **Graph Producer**:
    ```sh
    docker-compose run graph_producer
    ```

3. **Kafka Consumer**:
    ```sh
    docker-compose run kafka_consumer
    ```

## Running Scripts to Populate Dummy Data

### MySQL
```sh
docker exec -i mysql mysql -u root -prootpassword < ./data/dummy_clothes.sql
```

### Neo4j
```sh
docker exec -i neo4j cypher-shell -u neo4j -p password < ./data/dummy_users.cypher
```