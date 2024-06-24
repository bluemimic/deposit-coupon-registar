FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir /logs/

RUN apt-get update && apt-get install -y gettext && \
    apt install -y libzbar0 && \
    apt install -y python3-opencv

RUN python3 registar/manage.py collectstatic --noinput

COPY . .
