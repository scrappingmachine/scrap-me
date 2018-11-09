FROM python:3.6

WORKDIR /project
COPY main.py main.py
COPY src src
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt
RUN echo "#!/bin/bash\npython /project/main.py collector" > /usr/bin/collector
RUN echo "#!/bin/bash\npython /project/main.py worker" > /usr/bin/worker
RUN echo "#!/bin/bash\npython /project/main.py dispatcher --location-id 4" > /usr/bin/dispatcher
RUN chmod +x /usr/bin/collector
RUN chmod +x /usr/bin/worker
RUN chmod +x /usr/bin/dispatcher

ENV RABBITMQ_USER user
ENV RABBITMQ_PASSWORD user
ENV RABBITMQ_ADDR 127.0.0.1
ENV MINIO_USER user
ENV MINIO_PASSWORD user1234
ENV MINIO_ADDR 127.0.0.1
