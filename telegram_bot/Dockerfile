FROM python:3.8.7-alpine

COPY . /app
WORKDIR /app

RUN pip3 install -r requirements.txt

ARG ENGINE_IP
ARG ENGINE_PORT
ARG TELEGRAM_BOT_TOKEN

#RUN apk --no-cache add curl
CMD ["python3.8", "bot.py"]