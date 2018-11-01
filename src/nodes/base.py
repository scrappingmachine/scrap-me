import pika


class BaseNode(object):

    def __init__(self):
        credentials = pika.PlainCredentials('user', 'user')
        parameters = pika.ConnectionParameters(
            'localhost', 5672, '/', credentials, heartbeat_interval=0)
        self.connection = pika.BlockingConnection(parameters)

        self.channel = self.connection.channel()
