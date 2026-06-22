from collections.abc import Generator
import os

from dotenv import load_dotenv
from sqlmodel import Session, create_engine

load_dotenv()

db_url = os.getenv("DB_ADMIN")
if not db_url:
    raise RuntimeError("DB_ADMIN environment variable is required")

engine = create_engine(db_url, echo=True)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
