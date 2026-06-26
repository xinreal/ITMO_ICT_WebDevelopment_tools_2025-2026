from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import Engine
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session, create_engine

from lab_1.models import Hackathon, HackathonFormat


def _load_environment() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    for env_path in (
        repo_root / "lab_2" / ".env",
        repo_root / ".env",
        repo_root / "lab_1" / ".env",
    ):
        load_dotenv(env_path, override=False)


def get_database_url() -> str:
    _load_environment()
    database_url = os.getenv("DB_ADMIN")
    if not database_url:
        raise RuntimeError("DB_ADMIN environment variable is required")
    return database_url


def create_database_engine() -> Engine:
    return create_engine(get_database_url(), echo=False, pool_pre_ping=True)


def save_hackathon_from_page(url: str, page_title: str) -> int:
    engine = create_database_engine()
    hackathon = Hackathon(
        title=page_title,
        description=f"Imported from {url}",
        city="Online",
        format=HackathonFormat.online,
        duration_hours=1,
        organizer_id=None,
    )
    try:
        with Session(engine) as session:
            session.add(hackathon)
            session.commit()
            session.refresh(hackathon)
            if hackathon.id is None:
                raise RuntimeError("database did not return a new hackathon id")
            return hackathon.id
    except SQLAlchemyError as exc:
        raise RuntimeError(f"database error while saving {url}: {exc}") from exc
