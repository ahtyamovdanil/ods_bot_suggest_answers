FROM ubuntu:latest
RUN apt update
RUN apt install -y python3.8-dev
RUN apt install -y python3-pip

COPY . /app
WORKDIR /app

RUN pip3 install -r requirements.txt

ARG ENGINE_IP
ARG ENGINE_PORT
ARG TELEGRAM_BOT_TOKEN
ENV ENGINE_IP=$ENGINE_IP
ENV ENGINE_PORT=$ENGINE_PORT
ENV TELEGRAM_BOT_TOKEN=$TELEGRAM_BOT_TOKEN
RUN apt update
RUN apt install -y curl

CMD ["python3.8", "bot.py"]