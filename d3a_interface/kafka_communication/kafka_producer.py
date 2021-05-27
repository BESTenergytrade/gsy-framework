import json
from abc import ABC, abstractmethod

import logging
from zlib import compress

from kafka import KafkaProducer

from d3a_interface.kafka_communication import (
    KAFKA_URL, DEFAULT_KAFKA_URL, KAFKA_USERNAME, KAFKA_PASSWORD,
    KAFKA_COMMUNICATION_SECURITY_PROTOCOL, KAFKA_SASL_AUTH_MECHANISM, KAFKA_API_VERSION,
    create_kafka_new_ssl_context, KAFKA_TOPIC)

KAFKA_PUBLISH_RETRIES = 5
KAFKA_BUFFER_MEMORY_BYTES = 2048000000
KAFKA_MAX_REQUEST_SIZE_BYTES = 2048000000


def kafka_connection_factory():
    try:
        return KafkaConnection()
    except Exception:
        logging.info("Running without Kafka connection for simulation results.")
        return DisabledKafkaConnection()


class DisabledKafkaConnection(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def publish(self, results, job_id):
        pass

    @staticmethod
    @abstractmethod
    def is_enabled():
        return False


class KafkaConnection(DisabledKafkaConnection):
    def __init__(self):
        super().__init__()
        if KAFKA_URL != DEFAULT_KAFKA_URL:
            kwargs = {"bootstrap_servers": KAFKA_URL,
                      "sasl_plain_username": KAFKA_USERNAME,
                      "sasl_plain_password": KAFKA_PASSWORD,
                      "security_protocol": KAFKA_COMMUNICATION_SECURITY_PROTOCOL,
                      "ssl_context": create_kafka_new_ssl_context(),
                      "sasl_mechanism": KAFKA_SASL_AUTH_MECHANISM,
                      "api_version": KAFKA_API_VERSION,
                      "retries": KAFKA_PUBLISH_RETRIES,
                      "buffer_memory": KAFKA_BUFFER_MEMORY_BYTES,
                      "max_request_size": KAFKA_MAX_REQUEST_SIZE_BYTES}
        else:
            kwargs = {"bootstrap_servers": KAFKA_URL}

        self.producer = KafkaProducer(**kwargs)

    def publish(self, results, job_id):
        results = json.dumps(results).encode("utf-8")
        results = compress(results)
        self.producer.send(KAFKA_TOPIC, value=results, key=job_id.encode("utf-8"))

    @staticmethod
    def is_enabled():
        return True
