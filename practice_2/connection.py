from sqlmodel import SQLModel, Session, create_engine
import models

db_url = "postgresql://postgres:ksusus2002@localhost/hackathon_db"

engine = create_engine(db_url, echo=True)


def create_db_and_tables():
    print("TABLES IN METADATA:", SQLModel.metadata.tables.keys())
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session