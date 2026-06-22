from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from connection import get_session
from models import Participant
from schemas import ParticipantCreate, ParticipantPublic, ParticipantUpdate

router = APIRouter(prefix="/participants", tags=["participants"])


@router.post("/", response_model=ParticipantPublic)
def create_participant(
    participant: ParticipantCreate,
    session: Session = Depends(get_session),
) -> Participant:
    db_participant = Participant.model_validate(participant)
    session.add(db_participant)
    session.commit()
    session.refresh(db_participant)
    return db_participant


@router.get("/", response_model=list[ParticipantPublic])
def read_participants(session: Session = Depends(get_session)) -> list[Participant]:
    return list(session.exec(select(Participant)).all())


@router.get("/{participant_id}", response_model=ParticipantPublic)
def read_participant(
    participant_id: int,
    session: Session = Depends(get_session),
) -> Participant:
    participant = session.get(Participant, participant_id)
    if not participant:
        raise HTTPException(status_code=404, detail="Participant not found")
    return participant


@router.put("/{participant_id}", response_model=ParticipantPublic)
def update_participant(
    participant_id: int,
    participant: ParticipantUpdate,
    session: Session = Depends(get_session),
) -> Participant:
    db_participant = session.get(Participant, participant_id)
    if not db_participant:
        raise HTTPException(status_code=404, detail="Participant not found")

    db_participant.sqlmodel_update(participant.model_dump(exclude_unset=True))
    session.add(db_participant)
    session.commit()
    session.refresh(db_participant)
    return db_participant


@router.delete("/{participant_id}")
def delete_participant(
    participant_id: int,
    session: Session = Depends(get_session),
) -> dict[str, bool]:
    participant = session.get(Participant, participant_id)
    if not participant:
        raise HTTPException(status_code=404, detail="Participant not found")

    session.delete(participant)
    session.commit()
    return {"ok": True}
