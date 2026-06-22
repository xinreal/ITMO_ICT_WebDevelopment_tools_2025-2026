from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from connection import get_session
from models import ChallengeTask, Hackathon
from schemas import ChallengeTaskCreate, ChallengeTaskPublic, ChallengeTaskUpdate

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=ChallengeTaskPublic)
def create_task(
    task: ChallengeTaskCreate,
    session: Session = Depends(get_session),
) -> ChallengeTask:
    if task.hackathon_id is not None:
        hackathon = session.get(Hackathon, task.hackathon_id)
        if not hackathon:
            raise HTTPException(status_code=404, detail="Hackathon not found")

    db_task = ChallengeTask.model_validate(task)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@router.get("/", response_model=list[ChallengeTaskPublic])
def read_tasks(session: Session = Depends(get_session)) -> list[ChallengeTask]:
    return list(session.exec(select(ChallengeTask)).all())


@router.get("/{task_id}", response_model=ChallengeTaskPublic)
def read_task(
    task_id: int,
    session: Session = Depends(get_session),
) -> ChallengeTask:
    task = session.get(ChallengeTask, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{task_id}", response_model=ChallengeTaskPublic)
def update_task(
    task_id: int,
    task: ChallengeTaskUpdate,
    session: Session = Depends(get_session),
) -> ChallengeTask:
    db_task = session.get(ChallengeTask, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.hackathon_id is not None:
        hackathon = session.get(Hackathon, task.hackathon_id)
        if not hackathon:
            raise HTTPException(status_code=404, detail="Hackathon not found")

    db_task.sqlmodel_update(task.model_dump(exclude_unset=True))
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    session: Session = Depends(get_session),
) -> dict[str, bool]:
    task = session.get(ChallengeTask, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    session.delete(task)
    session.commit()
    return {"ok": True}
