from enum import Enum
from typing import Optional

from sqlmodel import SQLModel, Field, Relationship



class HackathonFormat(str, Enum):
    offline = "offline"
    online = "online"
    hybrid = "hybrid"


# many-to-many: участник <-> хакатон
class ParticipantHackathonLink(SQLModel, table=True):
    participant_id: int | None = Field(
        default=None,
        foreign_key="participant.id",
        primary_key=True
    )
    hackathon_id: int | None = Field(
        default=None,
        foreign_key="hackathon.id",
        primary_key=True
    )
    role_in_hackathon: str | None = None


class Organizer(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str
    email: str
    phone: str
    organization: str

    hackathons: list["Hackathon"] = Relationship(back_populates="organizer")


class Participant(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str
    email: str
    contact_number: str
    specialization: str

    hackathons: list["Hackathon"] = Relationship(
        back_populates="participants",
        link_model=ParticipantHackathonLink
    )


class Hackathon(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    city: str
    format: HackathonFormat
    duration_hours: int

    organizer_id: Optional[int] = Field(
        default=None,
        foreign_key="organizer.id"
    )

    organizer: Optional["Organizer"] = Relationship(back_populates="hackathons")
    participants: list["Participant"] = Relationship(
        back_populates="hackathons",
        link_model=ParticipantHackathonLink
    )
    tasks: list["ChallengeTask"] = Relationship(back_populates="hackathon")


class ChallengeTask(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    requirements: str
    evaluation_criteria: str

    hackathon_id: Optional[int] = Field(
        default=None,
        foreign_key="hackathon.id"
    )

    hackathon: Optional["Hackathon"] = Relationship(back_populates="tasks")