FROM python:3.8

WORKDIR /usr/src/app

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

ADD app.py .
ADD utils utils

CMD ["python", "app.py"]
