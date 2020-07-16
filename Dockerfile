FROM python:3.8

RUN pip install Flask gunicorn

COPY src/ app/
WORKDIR /app

ENV PORT 8080

CMD exec gunicorn --bind :$PORT --workers 1 --thread 8 app:app