FROM ubuntu:latest
RUN apt update
RUN apt install -y python3.8-dev
RUN apt install -y python3-pip
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
WORKDIR /usr/src/app
# COPY ./data/embeddings ./data/embeddings
# COPY ./data/prepared ./data/prepared
COPY ./app ./
RUN mkdir /root/.cache/torch
CMD ["python3.8", "engine_api.py"]