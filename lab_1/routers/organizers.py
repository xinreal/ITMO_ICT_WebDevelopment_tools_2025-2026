from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from connection import get_session
from models import Organizer
from schemas import OrganizerCreate, OrganizerPublic, OrganizerUpdate

router = APIRouter(prefix="/organizers", tags=["organizers"])


@router.post("/", response_model=OrganizerPublic)
def create_organizer(
    organizer: OrganizerCreate,
    session: Session = Depends(get_session),
) -> Organizer:
    db_organizer = Organizer.model_validate(organizer)
    session.add(db_organizer)
    session.commit()
    session.refresh(db_organizer)
    return db_organizer


@router.get("/", response_model=list[OrganizerPublic])
def read_organizers(session: Session = Depends(get_session)) -> list[Organizer]:
    return list(session.exec(select(Organizer)).all())


@router.get("/{organizer_id}", response_model=OrganizerPublic)
def read_organizer(
    organizer_id: int,
    session: Session = Depends(get_session),
) -> Organizer:
    organizer = session.get(Organizer, organizer_id)
    if not organizer:
        raise HTTPException(status_code=404, detail="Organizer not found")
    return organizer


@router.put("/{organizer_id}", response_model=OrganizerPublic)
def update_organizer(
    organizer_id: int,
    organizer: OrganizerUpdate,
    session: Session = Depends(get_session),
) -> Organizer:
    db_organizer = session.get(Organizer, organizer_id)
    if not db_organizer:
        raise HTTPException(status_code=404, detail="Organizer not found")

    db_organizer.sqlmodel_update(organizer.model_dump(exclude_unset=True))
    session.add(db_organizer)
    session.commit()
    session.refresh(db_organizer)
    return db_organizer


@router.delete("/{organizer_id}")
def delete_organizer(
    organizer_id: int,
    session: Session = Depends(get_session),
) -> dict[str, bool]:
    organizer = session.get(Organizer, organizer_id)
    if not organizer:
        raise HTTPException(status_code=404, detail="Organizer not found")

    session.delete(organizer)
    session.commit()
    return {"ok": True}
