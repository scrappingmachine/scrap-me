from src.nodes.base import BaseNode

import json
import os
import io
from minio import Minio
from minio.error import BucketAlreadyOwnedByYou
from minio.error import BucketAlreadyExists
import logging


class Collector(BaseNode):

    def __init__(self):
        super(Collector, self).__init__()
        user = os.environ["MINIO_ACCESS_KEY"]
        password = os.environ["MINIO_SECRET_KEY"]
        addr = os.environ["MINIO_ADDR"]

        self.minioClient = Minio(
            addr,
            access_key=user,
            secret_key=password,
            secure=False,
            region='us-east-1')

        try:
            self.minioClient.make_bucket("reviews")
        except BucketAlreadyOwnedByYou:
            pass
        except BucketAlreadyExists:
            pass

        self.channel.queue_declare(queue='scrap_result')
        self.channel.basic_consume(
            self.callback,
            queue='scrap_result',
            no_ack=True)

        self.channel.start_consuming()

    def callback(self, ch, method, properties, body):
        d = json.loads(body)
        print("Putting hotel to minio")
        self.minioClient.put_object(
            "reviews",
            d["name"],
            io.BytesIO(body),
            len(body),
            content_type="application/json")
