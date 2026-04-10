from enum import Enum
from pydantic import BaseModel, Field


class HackathonFormat(str, Enum):
    offline = "offline"
    online = "online"
    hybrid = "hybrid"


class Organizer(BaseModel):
    id: int
    full_name: str
    email: str
    phone: str
    organization: str


class ChallengeTask(BaseModel):
    id: int
    title: str
    description: str
    requirements: str
    evaluation_criteria: str


class Hackathon(BaseModel):
    id: int
    title: str
    description: str
    city: str
    format: HackathonFormat
    duration_hours: int
    organizer: Organizer
    tasks: list[ChallengeTask] = Field(default_factory=list)