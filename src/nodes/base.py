import pika
import os


class BaseNode(object):

    def __init__(self):
        user = os.environ["RABBITMQ_USER"]
        password = os.environ["RABBITMQ_PASSWORD"]
        addr = os.environ["RABBITMQ_ADDR"]

        credentials = pika.PlainCredentials(user, password)
        parameters = pika.ConnectionParameters(
            addr, 5672, '/', credentials, heartbeat_interval=0)
        self.connection = pika.BlockingConnection(parameters)

        self.channel = self.connection.channel()
