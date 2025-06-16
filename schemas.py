from pydantic import BaseModel
from datetime import datetime

# Define the format for incoming logs
class LogInput(BaseModel):
    source_ip: str
    username: str
    action: str
    status: str
    timestamp: datetime

class RawLogInput(BaseModel):
    raw_log: str