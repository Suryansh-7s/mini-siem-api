from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import SessionLocal
from models import LogEntry
from schemas import LogInput
from rules import detect_brute_force
from parser import parse_log_line
from schemas import RawLogInput


app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/ingest")
def ingest_log(log: LogInput, db: Session = Depends(get_db)):
    # Convert the validated input into a database object
    entry = LogEntry(
        source_ip=log.source_ip,
        username=log.username,
        action=log.action,
        status=log.status,
        timestamp=log.timestamp
    )
    db.add(entry)
    db.commit()
    return {"message": "✅ Log ingested successfully"}

@app.post("/ingest-raw")
def ingest_raw_log(raw: RawLogInput, db: Session = Depends(get_db)):
    parsed = parse_log_line(raw.raw_log)
    if not parsed:
        return {"message": "❌ Could not parse log"}

    entry = LogEntry(**parsed)
    db.add(entry)
    db.commit()
    return {"message": "✅ Raw log ingested and parsed", "parsed_data": parsed}

@app.get("/alerts")
def get_alerts(db: Session = Depends(get_db)):
    logs = db.query(LogEntry).all()
    alerts = detect_brute_force(logs)
    return {"alerts": alerts}