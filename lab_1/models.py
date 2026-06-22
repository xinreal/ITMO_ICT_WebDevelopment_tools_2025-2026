from enum import Enum

from sqlmodel import Field, Relationship, SQLModel


class HackathonFormat(str, Enum):
    offline = "offline"
    online = "online"
    hybrid = "hybrid"


class ParticipantHackathonLink(SQLModel, table=True):
    participant_id: int = Field(
        foreign_key="participant.id",
        primary_key=True,
    )
    hackathon_id: int = Field(
        foreign_key="hackathon.id",
        primary_key=True,
    )
    role_in_hackathon: str = Field(min_length=1)


class Organizer(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    full_name: str = Field(min_length=1)
    email: str = Field(min_length=1)
    phone: str = Field(min_length=1)
    organization: str = Field(min_length=1)

    hackathons: list["Hackathon"] = Relationship(back_populates="organizer")


class Participant(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    full_name: str = Field(min_length=1)
    email: str = Field(min_length=1)
    contact_number: str = Field(min_length=1)
    specialization: str = Field(min_length=1)

    hackathons: list["Hackathon"] = Relationship(
        back_populates="participants",
        link_model=ParticipantHackathonLink,
    )


class Hackathon(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(min_length=1)
    description: str = Field(min_length=1)
    city: str = Field(min_length=1)
    format: HackathonFormat
    duration_hours: int = Field(gt=0)

    organizer_id: int | None = Field(
        default=None,
        foreign_key="organizer.id",
    )

    organizer: Organizer | None = Relationship(back_populates="hackathons")
    participants: list[Participant] = Relationship(
        back_populates="hackathons",
        link_model=ParticipantHackathonLink,
    )
    tasks: list["ChallengeTask"] = Relationship(back_populates="hackathon")


class ChallengeTask(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(min_length=1)
    description: str = Field(min_length=1)
    requirements: str = Field(min_length=1)
    evaluation_criteria: str = Field(min_length=1)

    hackathon_id: int | None = Field(
        default=None,
        foreign_key="hackathon.id",
    )

    hackathon: Hackathon | None = Relationship(back_populates="tasks")


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True, min_length=1)
    email: str = Field(index=True, unique=True, min_length=1)
    full_name: str | None = Field(default=None, min_length=1)
    hashed_password: str = Field(min_length=1)
    is_active: bool = True
