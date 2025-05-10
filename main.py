from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel, validator
import uuid

from sqlalchemy import create_engine, Column, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DATABASE_URL = "postgresql://transactions_de3h_user:f9QOUCwn5lCKpGCERfFoqMlJ6vEh9vwR@dpg-d0f88b6uk2gs738jngkg-a.oregon-postgres.render.com/transactions_de3h"
engine = create_engine(DATABASE_URL)

# LOCAL TESTING:

### DATABASE_URL = "sqlite:///./payments.db"
### engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()



class Payment(Base):
    __tablename__ = "payments"

    payment_id = Column(String, primary_key=True, index=True)
    card_number = Column(String)
    amount = Column(Float)
    currency = Column(String)
    customer_name = Column(String)
    card_type = Column(String)
    timestamp = Column(String)
    status = Column(String)

Base.metadata.create_all(bind=engine)


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
    db = SessionLocal()
    payment_id = str(uuid.uuid4())

    if request.card_number.startswith("4"):
        card_type = "Visa"
    elif request.card_number.startswith("5"):
        card_type = "Mastercard"
    else:
        card_type = "Undefined"

    timestamp = datetime.now().isoformat()

    payment = Payment(
        payment_id=payment_id,
        card_number=request.card_number,
        amount=request.amount,
        currency=request.currency,
        customer_name=request.customer_name,
        card_type=card_type,
        timestamp=timestamp,
        status="authorized"
    )

    db.add(payment)
    db.commit()
    db.close()

    return {
        "payment_id": payment_id,
        "status": "Payment authorized",
        "card_type": card_type,
        "timestamp": timestamp
    }

@app.post("/refund/{payment_id}")
def refund(payment_id: str):
    db = SessionLocal()
    payment = db.query(Payment).filter(Payment.payment_id == payment_id).first()

    if payment:
        payment.status = "refunded"
        db.commit()
        db.close()
        return {"payment_id": payment_id, "status": "Payment refunded"}
    else:
        db.close()
        return {"error": "Payment not found"}



@app.get("/status/{payment_id}")
def get_status(payment_id: str):
    db = SessionLocal()
    payment = db.query(Payment).filter(Payment.payment_id == payment_id).first()
    db.close()

    if payment:
        return {
            "payment_id": payment.payment_id,
            "card_number": payment.card_number,
            "amount": payment.amount,
            "currency": payment.currency,
            "customer_name": payment.customer_name,
            "status": payment.status,
            "timestamp": payment.timestamp,
            "card_type": payment.card_type
        }
    else:
        return {"error": "Payment not found"}
