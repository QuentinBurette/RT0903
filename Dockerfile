FROM python:3.8-alpine

# set work directory
WORKDIR /mnt/c/Users/tinti/Desktop/rt0903-kubernetes

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /mnt/c/Users/tinti/Desktop/rt0903-kubernetes/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY . /mnt/c/Users/tinti/Desktop/rt0903-kubernetes

ENV FLASK_APP=main

ENTRYPOINT ["python3", "main.py"]