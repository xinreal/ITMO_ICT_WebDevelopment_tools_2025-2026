from typing import Optional

from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Session, SQLModel, select

from connection import create_db_and_tables, get_session
from models import (
    Organizer,
    Participant,
    Hackathon,
    ChallengeTask,
    ParticipantHackathonLink,
    HackathonFormat,
)

app = FastAPI(title="Hackathon API")


@app.get("/")
def root():
    return {"message": "Hackathon API is running"}


# =========================
# SCHEMAS
# =========================

class OrganizerCreate(SQLModel):
    full_name: str
    email: str
    phone: str
    organization: str


class OrganizerPublic(SQLModel):
    id: int
    full_name: str
    email: str
    phone: str
    organization: str


class ParticipantCreate(SQLModel):
    full_name: str
    email: str
    contact_number: str
    specialization: str


class ParticipantPublic(SQLModel):
    id: int
    full_name: str
    email: str
    contact_number: str
    specialization: str


class HackathonCreate(SQLModel):
    title: str
    description: str
    city: str
    format: HackathonFormat
    duration_hours: int
    organizer_id: Optional[int] = None


class HackathonPublic(SQLModel):
    id: int
    title: str
    description: str
    city: str
    format: HackathonFormat
    duration_hours: int
    organizer_id: Optional[int] = None


class ChallengeTaskCreate(SQLModel):
    title: str
    description: str
    requirements: str
    evaluation_criteria: str
    hackathon_id: Optional[int] = None


class ChallengeTaskPublic(SQLModel):
    id: int
    title: str
    description: str
    requirements: str
    evaluation_criteria: str
    hackathon_id: Optional[int] = None


class HackathonFull(SQLModel):
    id: int
    title: str
    description: str
    city: str
    format: HackathonFormat
    duration_hours: int
    organizer: Optional[OrganizerPublic] = None
    participants: list[ParticipantPublic] = []
    tasks: list[ChallengeTaskPublic] = []

class OrganizerUpdate(SQLModel):
    full_name: str | None = None
    email: str | None = None
    phone: str | None = None
    organization: str | None = None


class ParticipantUpdate(SQLModel):
    full_name: str | None = None
    email: str | None = None
    contact_number: str | None = None
    specialization: str | None = None


class HackathonUpdate(SQLModel):
    title: str | None = None
    description: str | None = None
    city: str | None = None
    format: HackathonFormat | None = None
    duration_hours: int | None = None
    organizer_id: int | None = None


class ChallengeTaskUpdate(SQLModel):
    title: str | None = None
    description: str | None = None
    requirements: str | None = None
    evaluation_criteria: str | None = None
    hackathon_id: int | None = None

# =========================
# ORGANIZERS
# =========================

@app.post("/organizers/", response_model=OrganizerPublic)
def create_organizer(
    organizer: OrganizerCreate,
    session: Session = Depends(get_session)
):
    db_organizer = Organizer.model_validate(organizer)
    session.add(db_organizer)
    session.commit()
    session.refresh(db_organizer)
    return db_organizer


@app.get("/organizers/", response_model=list[OrganizerPublic])
def read_organizers(session: Session = Depends(get_session)):
    organizers = session.exec(select(Organizer)).all()
    return organizers


@app.get("/organizers/{organizer_id}", response_model=OrganizerPublic)
def read_organizer(
    organizer_id: int,
    session: Session = Depends(get_session)
):
    organizer = session.get(Organizer, organizer_id)
    if not organizer:
        raise HTTPException(status_code=404, detail="Organizer not found")
    return organizer

@app.put("/organizers/{organizer_id}", response_model=OrganizerPublic)
def update_organizer(
    organizer_id: int,
    organizer: OrganizerUpdate,
    session: Session = Depends(get_session)
):
    db_organizer = session.get(Organizer, organizer_id)
    if not db_organizer:
        raise HTTPException(status_code=404, detail="Organizer not found")

    organizer_data = organizer.model_dump(exclude_unset=True)
    db_organizer.sqlmodel_update(organizer_data)

    session.add(db_organizer)
    session.commit()
    session.refresh(db_organizer)
    return db_organizer


@app.delete("/organizers/{organizer_id}")
def delete_organizer(
    organizer_id: int,
    session: Session = Depends(get_session)
):
    organizer = session.get(Organizer, organizer_id)
    if not organizer:
        raise HTTPException(status_code=404, detail="Organizer not found")

    session.delete(organizer)
    session.commit()
    return {"ok": True}


# =========================
# PARTICIPANTS
# =========================

@app.post("/participants/", response_model=ParticipantPublic)
def create_participant(
    participant: ParticipantCreate,
    session: Session = Depends(get_session)
):
    db_participant = Participant.model_validate(participant)
    session.add(db_participant)
    session.commit()
    session.refresh(db_participant)
    return db_participant


@app.get("/participants/", response_model=list[ParticipantPublic])
def read_participants(session: Session = Depends(get_session)):
    participants = session.exec(select(Participant)).all()
    return participants


@app.get("/participants/{participant_id}", response_model=ParticipantPublic)
def read_participant(
    participant_id: int,
    session: Session = Depends(get_session)
):
    participant = session.get(Participant, participant_id)
    if not participant:
        raise HTTPException(status_code=404, detail="Participant not found")
    return participant

@app.put("/participants/{participant_id}", response_model=ParticipantPublic)
def update_participant(
    participant_id: int,
    participant: ParticipantUpdate,
    session: Session = Depends(get_session)
):
    db_participant = session.get(Participant, participant_id)
    if not db_participant:
        raise HTTPException(status_code=404, detail="Participant not found")

    participant_data = participant.model_dump(exclude_unset=True)
    db_participant.sqlmodel_update(participant_data)

    session.add(db_participant)
    session.commit()
    session.refresh(db_participant)
    return db_participant


@app.delete("/participants/{participant_id}")
def delete_participant(
    participant_id: int,
    session: Session = Depends(get_session)
):
    participant = session.get(Participant, participant_id)
    if not participant:
        raise HTTPException(status_code=404, detail="Participant not found")

    session.delete(participant)
    session.commit()
    return {"ok": True}

# =========================
# HACKATHONS
# =========================

@app.post("/hackathons/", response_model=HackathonPublic)
def create_hackathon(
    hackathon: HackathonCreate,
    session: Session = Depends(get_session)
):
    if hackathon.organizer_id is not None:
        organizer = session.get(Organizer, hackathon.organizer_id)
        if not organizer:
            raise HTTPException(status_code=404, detail="Organizer not found")

    db_hackathon = Hackathon.model_validate(hackathon)
    session.add(db_hackathon)
    session.commit()
    session.refresh(db_hackathon)
    return db_hackathon


@app.get("/hackathons/", response_model=list[HackathonPublic])
def read_hackathons(session: Session = Depends(get_session)):
    hackathons = session.exec(select(Hackathon)).all()
    return hackathons


@app.get("/hackathons/{hackathon_id}", response_model=HackathonPublic)
def read_hackathon(
    hackathon_id: int,
    session: Session = Depends(get_session)
):
    hackathon = session.get(Hackathon, hackathon_id)
    if not hackathon:
        raise HTTPException(status_code=404, detail="Hackathon not found")
    return hackathon

@app.put("/hackathons/{hackathon_id}", response_model=HackathonPublic)
def update_hackathon(
    hackathon_id: int,
    hackathon: HackathonUpdate,
    session: Session = Depends(get_session)
):
    db_hackathon = session.get(Hackathon, hackathon_id)
    if not db_hackathon:
        raise HTTPException(status_code=404, detail="Hackathon not found")

    if hackathon.organizer_id is not None:
        organizer = session.get(Organizer, hackathon.organizer_id)
        if not organizer:
            raise HTTPException(status_code=404, detail="Organizer not found")

    hackathon_data = hackathon.model_dump(exclude_unset=True)
    db_hackathon.sqlmodel_update(hackathon_data)

    session.add(db_hackathon)
    session.commit()
    session.refresh(db_hackathon)
    return db_hackathon


@app.delete("/hackathons/{hackathon_id}")
def delete_hackathon(
    hackathon_id: int,
    session: Session = Depends(get_session)
):
    hackathon = session.get(Hackathon, hackathon_id)
    if not hackathon:
        raise HTTPException(status_code=404, detail="Hackathon not found")

    session.delete(hackathon)
    session.commit()
    return {"ok": True}

# =========================
# TASKS
# =========================

@app.post("/tasks/", response_model=ChallengeTaskPublic)
def create_task(
    task: ChallengeTaskCreate,
    session: Session = Depends(get_session)
):
    if task.hackathon_id is not None:
        hackathon = session.get(Hackathon, task.hackathon_id)
        if not hackathon:
            raise HTTPException(status_code=404, detail="Hackathon not found")

    db_task = ChallengeTask.model_validate(task)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@app.get("/tasks/", response_model=list[ChallengeTaskPublic])
def read_tasks(session: Session = Depends(get_session)):
    tasks = session.exec(select(ChallengeTask)).all()
    return tasks


@app.get("/tasks/{task_id}", response_model=ChallengeTaskPublic)
def read_task(
    task_id: int,
    session: Session = Depends(get_session)
):
    task = session.get(ChallengeTask, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/tasks/{task_id}", response_model=ChallengeTaskPublic)
def update_task(
    task_id: int,
    task: ChallengeTaskUpdate,
    session: Session = Depends(get_session)
):
    db_task = session.get(ChallengeTask, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.hackathon_id is not None:
        hackathon = session.get(Hackathon, task.hackathon_id)
        if not hackathon:
            raise HTTPException(status_code=404, detail="Hackathon not found")

    task_data = task.model_dump(exclude_unset=True)
    db_task.sqlmodel_update(task_data)

    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@app.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    session: Session = Depends(get_session)
):
    task = session.get(ChallengeTask, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    session.delete(task)
    session.commit()
    return {"ok": True}

# =========================
# MANY-TO-MANY
# participant <-> hackathon
# =========================

@app.post("/hackathons/{hackathon_id}/participants/{participant_id}")
def add_participant_to_hackathon(
    hackathon_id: int,
    participant_id: int,
    session: Session = Depends(get_session)
):
    hackathon = session.get(Hackathon, hackathon_id)
    if not hackathon:
        raise HTTPException(status_code=404, detail="Hackathon not found")

    participant = session.get(Participant, participant_id)
    if not participant:
        raise HTTPException(status_code=404, detail="Participant not found")

    existing_link = session.exec(
        select(ParticipantHackathonLink).where(
            ParticipantHackathonLink.hackathon_id == hackathon_id,
            ParticipantHackathonLink.participant_id == participant_id
        )
    ).first()

    if existing_link:
        return {"message": "Participant already added to this hackathon"}

    link = ParticipantHackathonLink(
        hackathon_id=hackathon_id,
        participant_id=participant_id
    )
    session.add(link)
    session.commit()

    return {"message": "Participant added to hackathon"}


# =========================
# NESTED VIEW
# =========================

@app.get("/hackathons/{hackathon_id}/full", response_model=HackathonFull)
def read_hackathon_full(
    hackathon_id: int,
    session: Session = Depends(get_session)
):
    hackathon = session.get(Hackathon, hackathon_id)
    if not hackathon:
        raise HTTPException(status_code=404, detail="Hackathon not found")

    organizer_obj = None
    if hackathon.organizer_id is not None:
        organizer = session.get(Organizer, hackathon.organizer_id)
        if organizer:
            organizer_obj = OrganizerPublic(
                id=organizer.id,
                full_name=organizer.full_name,
                email=organizer.email,
                phone=organizer.phone,
                organization=organizer.organization
            )

    tasks = session.exec(
        select(ChallengeTask).where(ChallengeTask.hackathon_id == hackathon_id)
    ).all()

    task_list = [
        ChallengeTaskPublic(
            id=task.id,
            title=task.title,
            description=task.description,
            requirements=task.requirements,
            evaluation_criteria=task.evaluation_criteria,
            hackathon_id=task.hackathon_id
        )
        for task in tasks
    ]

    links = session.exec(
        select(ParticipantHackathonLink).where(
            ParticipantHackathonLink.hackathon_id == hackathon_id
        )
    ).all()

    participants_list = []
    for link in links:
        participant = session.get(Participant, link.participant_id)
        if participant:
            participants_list.append(
                ParticipantPublic(
                    id=participant.id,
                    full_name=participant.full_name,
                    email=participant.email,
                    contact_number=participant.contact_number,
                    specialization=participant.specialization
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
        tasks=task_list
    )