from src.nodes.base import BaseNode
from src.generators.review import ReviewGenerator
from src.hotel import Hotel

import json
import re


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        return obj.__dict__


class Worker(BaseNode):

    def __init__(self):
        super(Worker, self).__init__()
        self.channel.queue_declare(queue='scrap_task')
        self.channel.queue_declare(queue='scrap_result')
        self.channel.basic_consume(
                self.callback,
                queue='scrap_task',
                no_ack=True)
        self.channel.start_consuming()

    def process_task(self, city_id, hotel_id):
        url = "https://pl.tripadvisor.com/Hotel_Review-g{}-d{}".format(
                city_id, hotel_id)
        soup = ReviewGenerator.get_soup(url)
        name = soup.find("h1", attrs={
            "class": "ui_header", "id": "HEADING"})
        name = name.text if name else None
        rating = soup.find("span", attrs={
            "class": "ui_bubble_rating"})
        if rating:
            rating = rating.get("class")[1]
            rating = re.search("bubble_(\d\d)", rating)                             #noqa: W605
            rating = rating.group(1) if rating else None
        else:
            rating = None
        reviews = list(ReviewGenerator(city_id, hotel_id))
        reviews = list(set(reviews))

        if reviews and name:
            return Hotel(name, rating, reviews, url)

    def callback(self, ch, method, properties, body):
        body = body.decode().split()
        hotel = self.process_task(body[0], body[1])

        if hotel:
            self.channel.basic_publish(
                    exchange='',
                    routing_key='scrap_result',
                    body=json.dumps(hotel, cls=CustomEncoder))
