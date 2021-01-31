FROM python:3.8.7-alpine

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

ARG ENGINE_IP
ARG ENGINE_PORT
ARG BOT_TOKEN

CMD ["python", "bot.py"]