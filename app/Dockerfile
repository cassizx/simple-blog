FROM python:3.9-slim

WORKDIR /usr/backend/

RUN groupadd --gid 2000 app \
    && useradd --uid 2000 --gid app --shell /bin/bash --create-home app

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY --chown=app:app . .

USER app

ENTRYPOINT ["python3"]

CMD ["run.py"]