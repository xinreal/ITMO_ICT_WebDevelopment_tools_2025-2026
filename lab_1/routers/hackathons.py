from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from connection import get_session
from models import ChallengeTask, Hackathon, Organizer, Participant, ParticipantHackathonLink
from schemas import (
    ChallengeTaskPublic,
    HackathonCreate,
    HackathonFull,
    HackathonPublic,
    HackathonUpdate,
    OrganizerPublic,
    ParticipantHackathonCreate,
    ParticipantHackathonPublic,
    ParticipantInHackathon,
)

router = APIRouter(prefix="/hackathons", tags=["hackathons"])


@router.post("/", response_model=HackathonPublic)
def create_hackathon(
    hackathon: HackathonCreate,
    session: Session = Depends(get_session),
) -> Hackathon:
    if hackathon.organizer_id is not None:
        organizer = session.get(Organizer, hackathon.organizer_id)
        if not organizer:
            raise HTTPException(status_code=404, detail="Organizer not found")

    db_hackathon = Hackathon.model_validate(hackathon)
    session.add(db_hackathon)
    session.commit()
    session.refresh(db_hackathon)
    return db_hackathon


@router.get("/", response_model=list[HackathonPublic])
def read_hackathons(session: Session = Depends(get_session)) -> list[Hackathon]:
    return list(session.exec(select(Hackathon)).all())


@router.get("/{hackathon_id}", response_model=HackathonPublic)
def read_hackathon(
    hackathon_id: int,
    session: Session = Depends(get_session),
) -> Hackathon:
    hackathon = session.get(Hackathon, hackathon_id)
    if not hackathon:
        raise HTTPException(status_code=404, detail="Hackathon not found")
    return hackathon


@router.put("/{hackathon_id}", response_model=HackathonPublic)
def update_hackathon(
    hackathon_id: int,
    hackathon: HackathonUpdate,
    session: Session = Depends(get_session),
) -> Hackathon:
    db_hackathon = session.get(Hackathon, hackathon_id)
    if not db_hackathon:
        raise HTTPException(status_code=404, detail="Hackathon not found")

    if hackathon.organizer_id is not None:
        organizer = session.get(Organizer, hackathon.organizer_id)
        if not organizer:
            raise HTTPException(status_code=404, detail="Organizer not found")

    db_hackathon.sqlmodel_update(hackathon.model_dump(exclude_unset=True))
    session.add(db_hackathon)
    session.commit()
    session.refresh(db_hackathon)
    return db_hackathon


@router.delete("/{hackathon_id}")
def delete_hackathon(
    hackathon_id: int,
    session: Session = Depends(get_session),
) -> dict[str, bool]:
    hackathon = session.get(Hackathon, hackathon_id)
    if not hackathon:
        raise HTTPException(status_code=404, detail="Hackathon not found")

    session.delete(hackathon)
    session.commit()
    return {"ok": True}


@router.post(
    "/{hackathon_id}/participants/{participant_id}",
    response_model=ParticipantHackathonPublic,
)
def add_participant_to_hackathon(
    hackathon_id: int,
    participant_id: int,
    link_data: ParticipantHackathonCreate,
    session: Session = Depends(get_session),
) -> ParticipantHackathonLink:
    hackathon = session.get(Hackathon, hackathon_id)
    if not hackathon:
        raise HTTPException(status_code=404, detail="Hackathon not found")

    participant = session.get(Participant, participant_id)
    if not participant:
        raise HTTPException(status_code=404, detail="Participant not found")

    existing_link = session.exec(
        select(ParticipantHackathonLink).where(
            ParticipantHackathonLink.hackathon_id == hackathon_id,
            ParticipantHackathonLink.participant_id == participant_id,
        )
    ).first()
    if existing_link:
        raise HTTPException(
            status_code=409,
            detail="Participant already added to this hackathon",
        )

    link = ParticipantHackathonLink(
        hackathon_id=hackathon_id,
        participant_id=participant_id,
        role_in_hackathon=link_data.role_in_hackathon,
    )
    session.add(link)
    session.commit()
    session.refresh(link)
    return link


@router.delete("/{hackathon_id}/participants/{participant_id}")
def delete_participant_from_hackathon(
    hackathon_id: int,
    participant_id: int,
    session: Session = Depends(get_session),
) -> dict[str, bool]:
    link = session.exec(
        select(ParticipantHackathonLink).where(
            ParticipantHackathonLink.hackathon_id == hackathon_id,
            ParticipantHackathonLink.participant_id == participant_id,
        )
    ).first()
    if not link:
        raise HTTPException(status_code=404, detail="Participant link not found")

    session.delete(link)
    session.commit()
    return {"ok": True}


@router.get("/{hackathon_id}/full", response_model=HackathonFull)
def read_hackathon_full(
    hackathon_id: int,
    session: Session = Depends(get_session),
) -> HackathonFull:
    hackathon = session.get(Hackathon, hackathon_id)
    if not hackathon:
        raise HTTPException(status_code=404, detail="Hackathon not found")

    organizer_obj = None
    if hackathon.organizer_id is not None:
        organizer = session.get(Organizer, hackathon.organizer_id)
        if organizer:
            organizer_obj = OrganizerPublic.model_validate(organizer)

    tasks = session.exec(
        select(ChallengeTask).where(ChallengeTask.hackathon_id == hackathon_id)
    ).all()
    task_list = [ChallengeTaskPublic.model_validate(task) for task in tasks]

    links = session.exec(
        select(ParticipantHackathonLink).where(
            ParticipantHackathonLink.hackathon_id == hackathon_id,
        )
    ).all()
    participants_list: list[ParticipantInHackathon] = []
    for link in links:
        participant = session.get(Participant, link.participant_id)
        if participant:
            participants_list.append(
                ParticipantInHackathon(
                    id=participant.id,
                    full_name=participant.full_name,
                    email=participant.email,
                    contact_number=participant.contact_number,
                    specialization=participant.specialization,
                    role_in_hackathon=link.role_in_hackathon,
                )
            )

    return HackathonFull(
        id=hackathon.id,
        title=hackathon.title,
        description=hackathon.description,
        city=hackathon.city,
        format=hackathon.format,
        duration_hours=hackathon.duration_hours,
        organizer=organizer_obj,
        participants=participants_list,
        tasks=task_list,
    )
