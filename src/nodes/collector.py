from src.nodes.base import BaseNode

import json
import io
from minio import Minio
from minio.error import BucketAlreadyOwnedByYou
from minio.error import BucketAlreadyExists


class Collector(BaseNode):

    def __init__(self):
        super(Collector, self).__init__()

        self.minioClient = Minio(
                "172.17.0.2:9000",
                access_key="user",
                secret_key="user1234",
                secure=False)

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
        self.minioClient.put_object(
                "reviews",
                d["name"],
                io.BytesIO(body),
                len(body),
                content_type="application/json")
