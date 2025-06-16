from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime

class LogEntry(Base):
    __tablename__ = "log_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    source_ip = Column(String)
    username = Column(String)
    action = Column(String)
    status = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
