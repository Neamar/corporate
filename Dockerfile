from python:2.7

ENV PYTHONUNBUFFERED=TRUE

WORKDIR /opt
COPY requirements.txt /opt
RUN pip install -r requirements.txt

COPY . /opt
