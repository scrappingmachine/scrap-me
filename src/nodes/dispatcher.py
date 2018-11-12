from src.nodes.base import BaseNode
from src.generators.hotel import HotelGenerator
import logging


class Dispatcher(BaseNode):

    def __init__(self, location_id):
        super(Dispatcher, self).__init__()
        self.location_id = location_id
        self.channel.queue_declare(queue='scrap_task')
        self.__start()

    def __start(self):

        for task in HotelGenerator(self.location_id):
            logging.info(f"New task showed up: {task}")
            self.channel.basic_publish(
                exchange='',
                routing_key='scrap_task',
                body=" ".join(task))
        self.connection.close()
