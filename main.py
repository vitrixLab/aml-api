import uuid
from fastapi import FastAPI, Request, Depends, HTTPException
from database import SessionLocal, engine, Base
from models import Transaction
from schemas import TransactionRequest
from rules_engine import evaluate_transaction
from logging_config import logger
from idempotency import get_idempotent, store_idempotent
import logging
import traceback

# Set up basic logging for startup
logging.basicConfig(level=logging.INFO)

# API version constant (can be read from environment or file)
API_VERSION = "1.0.0"
SERVICE_NAME = "AML/Fraud demo API"

app = FastAPI(title=SERVICE_NAME, version=API_VERSION)

# ---------- Startup Event ----------
@app.on_event("startup")
def init_db():
    """Create database tables on startup."""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created/verified.")
    except Exception as e:
        logger.error(f"Failed to create database tables: {e}")
        raise

# ---------- Database Dependency ----------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------- Middleware ----------
# @app.middleware("http")
# async def correlation_id(request: Request, call_next):
#     correlation = request.headers.get("X-Correlation-ID") or str(uuid.uuid4())
#     request.state.cid = correlation
#     response = await call_next(request)
#     response.headers["X-Correlation-ID"] = correlation
#     return response

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request started: {request.method} {request.url.path}")
    try:
        response = await call_next(request)
        logger.info(f"Request finished: {request.method} {request.url.path} - Status: {response.status_code}")
        return response
    except Exception as e:
        logger.error(f"Request failed: {request.method} {request.url.path} - Error: {e}\n{traceback.format_exc()}")
        raise

# ---------- Routes ----------
@app.get("/")
def root():
    """Root endpoint with API information."""
    return {
        "service": SERVICE_NAME,
        "version": API_VERSION,
        "description": "API for evaluating financial transactions against AML rules",
        "endpoints": {
            "/health": "Health check",
            "/evaluate": "Submit a transaction for evaluation (POST)",
            "/": "This information"
        },
        "documentation": "/docs"  # FastAPI automatic docs
    }

# @app.post("/evaluate")
# def evaluate(tx: TransactionRequest, request: Request):
#     # Skip DB entirely
#     return {"message": "evaluate would run here"}

@app.post("/evaluate")
def evaluate(tx: TransactionRequest, request: Request, db=Depends(get_db)):
    try:
        idempotency_key = request.headers.get("Idempotency-Key")

        # Idempotency check
        if idempotency_key:
            cached = get_idempotent(db, idempotency_key)
            if cached:
                return cached

        # Prepare payload and evaluate
        payload = tx.model_dump()
        result = evaluate_transaction(payload)   # from rules_engine.py

        # Extract fields from the evaluation result
        # (adjust key names if your rules_engine returns different ones)
        risk_score = result.get('score', 0)                 # default to 0 if missing
        decision = result.get('decision', 'REVIEW')         # default to REVIEW
        # The full result is already a dict; we'll store it as JSON

        # Generate transaction ID if not present in payload
        transaction_id = payload.get('id') or str(uuid.uuid4())

        # Create transaction with all fields
        transaction = Transaction(
            id=transaction_id,
            **payload,                     # input fields (account_id, amount, country, etc.)
            risk_score=risk_score,
            decision=decision,
            result=result                   # store full result as JSON
        )

        db.add(transaction)
        db.commit()
        db.refresh(transaction)

        # Store idempotent response (the full result)
        # After creating and committing the transaction
        full_response = {
            "transaction_id": transaction.id,
            **result   # result from evaluate_transaction
        }
        
        if idempotency_key:
            # Store the full response instead of just result
            store_idempotent(db, idempotency_key, full_response)
        
        return full_response

    except Exception as e:
        logger.error(f"Evaluation failed: {e}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Evaluation failed")
    
@app.get("/health")
def health():
    return {"status": "OK"}