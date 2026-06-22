from sqlmodel import Field, SQLModel

from models import HackathonFormat


class OrganizerCreate(SQLModel):
    full_name: str = Field(min_length=1)
    email: str = Field(min_length=1)
    phone: str = Field(min_length=1)
    organization: str = Field(min_length=1)


class OrganizerPublic(SQLModel):
    id: int
    full_name: str
    email: str
    phone: str
    organization: str


class OrganizerUpdate(SQLModel):
    full_name: str | None = Field(default=None, min_length=1)
    email: str | None = Field(default=None, min_length=1)
    phone: str | None = Field(default=None, min_length=1)
    organization: str | None = Field(default=None, min_length=1)


class ParticipantCreate(SQLModel):
    full_name: str = Field(min_length=1)
    email: str = Field(min_length=1)
    contact_number: str = Field(min_length=1)
    specialization: str = Field(min_length=1)


class ParticipantPublic(SQLModel):
    id: int
    full_name: str
    email: str
    contact_number: str
    specialization: str


class ParticipantUpdate(SQLModel):
    full_name: str | None = Field(default=None, min_length=1)
    email: str | None = Field(default=None, min_length=1)
    contact_number: str | None = Field(default=None, min_length=1)
    specialization: str | None = Field(default=None, min_length=1)


class HackathonCreate(SQLModel):
    title: str = Field(min_length=1)
    description: str = Field(min_length=1)
    city: str = Field(min_length=1)
    format: HackathonFormat
    duration_hours: int = Field(gt=0)
    organizer_id: int | None = None


class HackathonPublic(SQLModel):
    id: int
    title: str
    description: str
    city: str
    format: HackathonFormat
    duration_hours: int
    organizer_id: int | None = None


class HackathonUpdate(SQLModel):
    title: str | None = Field(default=None, min_length=1)
    description: str | None = Field(default=None, min_length=1)
    city: str | None = Field(default=None, min_length=1)
    format: HackathonFormat | None = None
    duration_hours: int | None = Field(default=None, gt=0)
    organizer_id: int | None = None


class ChallengeTaskCreate(SQLModel):
    title: str = Field(min_length=1)
    description: str = Field(min_length=1)
    requirements: str = Field(min_length=1)
    evaluation_criteria: str = Field(min_length=1)
    hackathon_id: int | None = None


class ChallengeTaskPublic(SQLModel):
    id: int
    title: str
    description: str
    requirements: str
    evaluation_criteria: str
    hackathon_id: int | None = None


class ChallengeTaskUpdate(SQLModel):
    title: str | None = Field(default=None, min_length=1)
    description: str | None = Field(default=None, min_length=1)
    requirements: str | None = Field(default=None, min_length=1)
    evaluation_criteria: str | None = Field(default=None, min_length=1)
    hackathon_id: int | None = None


class ParticipantHackathonCreate(SQLModel):
    role_in_hackathon: str = Field(min_length=1)


class ParticipantHackathonPublic(SQLModel):
    participant_id: int
    hackathon_id: int
    role_in_hackathon: str


class ParticipantInHackathon(ParticipantPublic):
    role_in_hackathon: str


class HackathonFull(SQLModel):
    id: int
    title: str
    description: str
    city: str
    format: HackathonFormat
    duration_hours: int
    organizer: OrganizerPublic | None = None
    participants: list[ParticipantInHackathon] = Field(default_factory=list)
    tasks: list[ChallengeTaskPublic] = Field(default_factory=list)


class UserRegister(SQLModel):
    username: str = Field(min_length=1)
    email: str = Field(min_length=1)
    full_name: str | None = Field(default=None, min_length=1)
    password: str = Field(min_length=1)


class UserLogin(SQLModel):
    username: str = Field(min_length=1)
    password: str = Field(min_length=1)


class UserPublic(SQLModel):
    id: int
    username: str
    email: str
    full_name: str | None = None
    is_active: bool


class Token(SQLModel):
    access_token: str
    token_type: str


class ChangePasswordRequest(SQLModel):
    old_password: str = Field(min_length=1)
    new_password: str = Field(min_length=1)
