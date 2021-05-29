FROM python:3.9-slim

WORKDIR /usr/backend/

RUN apt update &&  \
    apt install -y \
    curl && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .