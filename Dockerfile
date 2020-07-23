from python:2.7

RUN apt-get update && apt-get install libpq-dev -y

ENV PYTHONUNBUFFERED=TRUE

WORKDIR /opt
COPY requirements.txt /opt
RUN pip install -r requirements.txt

COPY . /opt
