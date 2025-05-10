FROM python:3.10

WORKDIR /app

COPY . /app

RUN pip install fastapi uvicorn sqlalchemy psycopg2-binary

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port $PORT"]
