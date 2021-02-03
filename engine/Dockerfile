FROM python:3.8.7-slim-buster as base-image

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt


FROM python:3.8.7-slim-buster as build-image

COPY --from=base-image /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /usr/src/app
#ADD https://www.dropbox.com/s/tmeqz5uhz7qfji2/edu_courses.pkl ./data/embeddings/
#ADD https://www.dropbox.com/s/23tqbs4qsez30x4/edu_courses.tsv ./data/prepared/
COPY ./data/embeddings ./data/embeddings
COPY ./data/prepared ./data/prepared
COPY ./app ./
EXPOSE 5000

CMD ["python", "engine_api.py"]