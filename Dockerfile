FROM python:3.10-slim

RUN \
    set -x \
    && buildDeps="build-essential git" \
    && apt-get update \
    && apt-get install -y $buildDeps

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

RUN apt-get remove -y build-essential git 

WORKDIR /app

COPY ./src /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]