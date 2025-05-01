from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel, validator
import uuid


app = FastAPI()

class PaymentRequest(BaseModel):
    card_number: str
    amount: float
    currency: str
    customer_name: str

    @validator("card_number")
    def validate_card_number(cls, v):
        if not v.isdigit() or len(v) != 16:
            raise ValueError("Card number must be 16 digits")
        return v

payments_db = {}

@app.post("/payment")
def create_payment(request: PaymentRequest):
    payment_id = str(uuid.uuid4())

    if request.card_number.startswith("4"):
        card_type = "Visa"
    elif request.card_number.startswith("5"):
        card_type = "Mastercard"
    else:
        card_type = "Unknown"

    timestamp = datetime.now().isoformat()

    payments_db[payment_id] = {
        "card_number": request.card_number,
        "amount": request.amount,
        "currency": request.currency,
        "customer_name": request.customer_name,
        "status": "authorized"
    }
    return {"payment_id": payment_id, 
            "status": "Payment authorized",
            "card_type": card_type,
            "timestamp": timestamp}

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
