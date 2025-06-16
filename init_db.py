from database import Base, engine
from models import LogEntry

# This will create the logs.db file and the log_entries table
Base.metadata.create_all(bind=engine)

print("✅ Database initialized.")