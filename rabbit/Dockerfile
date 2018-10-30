FROM rabbitmq:3.7.5-management

RUN apt-get update && apt-get install -y \
    apt-utils \
    iputils-ping \
    locales \
    locales-all \ 
    wget && \
    rm -rf /var/lib/apt/lists/*

RUN rabbitmq-plugins enable rabbitmq_management

ENV RABBITMQ_USER user
ENV RABBITMQ_PASSWORD user

EXPOSE 5672
EXPOSE 15672

ADD init.sh /init.sh
RUN ["chmod", "+x", "/init.sh"]
ENTRYPOINT ["/init.sh"]
