from sqlalchemy import Column, String, Float, Integer, DateTime, JSON  # add JSON
from sqlalchemy.sql import func
from database import Base

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(String, primary_key=True)
    account_id = Column(String, index=True)
    amount = Column(Float)
    country = Column(String)
    risk_score = Column(Integer)
    decision = Column(String)
    result = Column(JSON)  # new column to store the full evaluation output
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class IdempotencyRecord(Base):
    __tablename__ = "idempotency"
    key = Column(String, primary_key=True)
    response = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
