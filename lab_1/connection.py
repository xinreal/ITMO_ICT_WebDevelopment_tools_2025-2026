from sqlmodel import SQLModel, Session, create_engine
import models
import os
from dotenv import load_dotenv

load_dotenv()

db_url = os.getenv("DB_ADMIN")
if not db_url:
    raise ValueError("DB_ADMIN not found in .env")

engine = create_engine(db_url, echo=True)


def get_session():
    with Session(engine) as session:
        yield session