# Payments API

A RESTful API for simulating payment flows, including authorization, refund, transaction status query, and settlement file generation. Built with FastAPI, SQLite, and Docker, simulating real-world acquirer/processor behavior.

---

## Features

- Create a payment (`POST /payment`)
- Refund a payment (`POST /refund/{payment_id}`)
- Retrieve payment status (`GET /status/{payment_id}`)

---

## Tech Stack

- Python 3.10
- FastAPI
- SQLite (via SQLAlchemy)
- Docker
- Uvicorn (ASGI server)

---

## Running Locally with Docker

```bash
docker build -t mock-payments-api .
docker run -d --restart always -p 8000:8000 mock-payments-api
```

Then access:
http://localhost:8000/docs

---

## Public API

This API is deployed using Docker + Render.
Access it here:
https://payments-api-9127.onrender.com/docs


## Example Payload

{
  "card_number": "4111111111111111",
  "amount": 150.00,
  "currency": "USD",
  "customer_name": "Maria Oliveira"
}

## Author

Developed by Antonio Clóvis Pacheco Neto.
This project is part of my personal portfolio, simulating real payment processing flows typically used by acquirers and processors.