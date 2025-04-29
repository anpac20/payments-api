from fastapi import FastAPI
from pydantic import BaseModel
import uuid

app = FastAPI()

class PaymentRequest(BaseModel):
    card_number: str
    amount: float
    currency: str
    customer_name: str

payments_db = {}

@app.post("/payment")
def create_payment(request: PaymentRequest):
    payment_id = str(uuid.uuid4())
    payments_db[payment_id] = {
        "card_number": request.card_number,
        "amount": request.amount,
        "currency": request.currency,
        "customer_name": request.customer_name,
        "status": "authorized"
    }
    return {"payment_id": payment_id, "status": "Payment authorized"}

@app.post("/refund/{payment_id}")
def refund_payment(payment_id: str):
    if payment_id in payments_db:
        payments_db[payment_id]["status"] = "refunded"
        return {"payment_id": payment_id, "status": "Payment refunded"}
    else:
        return {"error": "Payment not found"}

@app.get("/status/{payment_id}")
def get_status(payment_id: str):
    if payment_id in payments_db:
        return payments_db[payment_id]
    else:
        return {"error": "Payment not found"}
