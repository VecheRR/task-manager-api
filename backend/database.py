from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import time

DATABASE_URL = "postgresql://user:password@db:5432/tasks_db"

for _ in range(10):
    try:
        engine = create_engine(DATABASE_URL)
        engine.connect()
        print("DB connected")
        break
    except Exception:
        print("DB not ready, retrying...")
        time.sleep(2)
else:
    raise Exception("DB connection failed")

SessionLocal = sessionmaker(bind=engine)