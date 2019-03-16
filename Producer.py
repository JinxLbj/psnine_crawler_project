import json

from kafka import KafkaProducer


class KafkaFactory:
    producer = None

    @staticmethod
    def init():
        global producer
        producer = KafkaProducer(bootstrap_servers='10.96.129.36:9092')
    @staticmethod
    def send(msg):
        global producer
        producer.send('EntryRecord', msg.encode('utf-8'))
    @staticmethod
    def close():
        global producer
        producer.close()
