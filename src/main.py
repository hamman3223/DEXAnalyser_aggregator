from confluent_kafka import Consumer
from models import *
from json import loads
from socket import gethostname
from dotenv import load_dotenv
from os import getenv
from typing import (List, Dict)
from loguru import logger

loguru = logger
load_dotenv()

class Storage(object):
    def __init__(self, topic: str):
        self.topic = topic

    def __enter__(self):
        kafka_configuration = {'bootstrap.servers': f"{getenv('KAFKA_HOST')}:{getenv('KAFKA_PORT')}",
                               "group.id": f"aggregator-{self.topic}",
                               "client.id": gethostname()}
        self.consumer = Consumer(kafka_configuration)
        self.consumer.subscribe([self.topic])
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.consumer.close()


class Aggregator:

    @staticmethod
    def fetchOrders():
        ...

    @staticmethod
    def aggregate(topic: str):
        with Storage(topic) as deps:
            while True:
                msg = deps.consumer.poll(1.0)

                if msg is None:
                    ...
                elif msg.error():
                    logger.error(f"Received an error when trying to poll from kafka {msg.error()}")
                elif msg:
                    data: str = msg.value().decode("utf-8")
                    data: List[Dict] = list(loads(data))

                    # TODO!: Передавать тип ордера в ввиде аргумента aggregate, чтобы data: List[Order]
                    data: List[LinchOrder] = list(map(lambda order: LinchOrder(**order), data))
                    return data

Aggregator.aggregate(topic="linch-collector")
