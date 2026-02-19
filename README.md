# AML/Fraud Detection API

A lightweight, high‑performance API for real‑time anti‑money laundering (AML) and fraud screening. Designed to showcase industry‑relevant skills in financial compliance, this service evaluates transaction payloads against a set of configurable rules:

- **Amount threshold** – flags high‑value transactions  
- **Country risk** – blocks or reviews transactions from high‑risk jurisdictions (e.g., IRAN, NORTH_KOREA, SYRIA)  

Each evaluation returns a **risk score**, a **decision** (APPROVE/REVIEW/BLOCK), a list of **triggered rules**, and a human‑readable **rationale** for audit trails.

### Features
- ✅ **Idempotent endpoints** – prevent duplicate processing with Idempotency-Key headers  
- ✅ **Structured logging** – for monitoring and debugging  
- ✅ **Persistent storage** – transactions stored in SQLite with full evaluation result as JSON  
- ✅ **Ready for deployment** – tested on PythonAnywhere (free tier)  
- ✅ **Clean, maintainable code** – follows FastAPI best practices  

### Tech Stack
- **Framework**: FastAPI (Python 3.13)  
- **Database**: SQLAlchemy ORM + SQLite  
- **Tools**: a2wsgi (for WSGI deployment), custom idempotency middleware  
- **Deployment**: PythonAnywhere

### Live Demo
Base URL: `https://citrixlabph.pythonanywhere.com`  
Try it with curl:
```bash
curl -X POST "https://citrixlabph.pythonanywhere.com/evaluate" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: test-123" \
  -d '{"account_id":"1234Z","amount":100000,"country":"IRAN"}'
```

---

# Future Enhancements
- Extend rule engine (e.g., velocity checks, ML integration)

- Add PostgreSQL support for production

- Containerize with Docker


### snippet of aml-api
AML/Fraud detection API built with FastAPI. Evaluates transactions against risk rules (amount thresholds, high‑risk countries) and returns a risk score, decision, and audit trail. Features idempotency and SQLite persistence.