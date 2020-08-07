FROM python:3.6

ADD . /blutv_challenge
WORKDIR /blutv_challenge

RUN pip install -r requirements.txt
COPY . /blutv_challenge

ENV SECRET_KEY="123123"
ENV MONGO_HOST="localhost"
ENV REDIS_HOST="localhost"
ENV REDIS_PORT=6379
ENV MONGO_PORT=27017

ENTRYPOINT [ "python" ]

CMD [ "application.py" ]
