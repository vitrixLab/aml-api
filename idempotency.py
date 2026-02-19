from models import IdempotencyRecord
import json

def get_idempotent(db, key):
    record = db.query(IdempotencyRecord).filter(IdempotencyRecord.key == key).first()
    if record:
        return json.loads(record.response)
    return None

def store_idempotent(db, key, response):
    import json
    record = IdempotencyRecord(key=key, response=json.dumps(response))
    db.add(record)
    db.commit()
