from src.nodes.base import BaseNode
from src.generators.hotel import HotelGenerator


class Dispatcher(BaseNode):

    def __init__(self):
        super(Dispatcher, self).__init__()
        self.channel.queue_declare(queue='scrap_task')
        self.__start()

    def __start(self):

        for task in HotelGenerator(274723):
            self.channel.basic_publish(
                    exchange='',
                    routing_key='scrap_task',
                    body=" ".join(task))

        self.connection.close()
