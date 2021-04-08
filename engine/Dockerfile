FROM python:3.8.7-slim-buster as base-image

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt


FROM python:3.8.7-slim-buster as build-image
RUN apt update && apt install -y zip
ADD https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip ./awscliv2.zip
RUN unzip awscliv2.zip
RUN ./aws/install

COPY --from=base-image /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY


ENV AWS_DEFAULT_REGION=ru-central1
ENV PYTHONPATH "${PYTHONPATH}:/usr/src/"

WORKDIR /usr/src/
COPY . ./
RUN aws --endpoint-url=https://storage.yandexcloud.net \
    s3 cp --recursive s3://odsbot/prod/ ./app/data

CMD ["python", "app/main.py"]
