from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .database import engine, get_db
from . import models, schemas

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="UnifyAI - Optimized Duplicate Detection")


@app.get("/")
def root():
    return {"message": "UnifyAI running 🚀"}


@app.post("/ingest", response_model=schemas.CustomerResponse)
def ingest_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):

    existing_email = db.query(models.Customer).filter(
        models.Customer.email == customer.email
    ).first()

    if existing_email:
        raise HTTPException(status_code=409, detail="Duplicate detected (Email match)")

    existing_phone = db.query(models.Customer).filter(
        models.Customer.phone == customer.phone
    ).first()

    if existing_phone:
        raise HTTPException(status_code=409, detail="Duplicate detected (Phone match)")

    new_customer = models.Customer(
        name=customer.name,
        email=customer.email,
        phone=customer.phone
    )

    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    return new_customer


@app.get("/customers", response_model=List[schemas.CustomerResponse])
def get_customers(db: Session = Depends(get_db)):
    return db.query(models.Customer).all()


@app.post("/reset")
def reset_database(db: Session = Depends(get_db)):
    db.query(models.Customer).delete()
    db.commit()
    return {"message": "Database reset successful"}