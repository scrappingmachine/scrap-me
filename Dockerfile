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
