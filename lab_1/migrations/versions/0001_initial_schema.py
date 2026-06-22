"""initial schema

Revision ID: 0001_initial_schema
Revises:
Create Date: 2026-06-17 00:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0001_initial_schema"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


hackathon_format = sa.Enum("offline", "online", "hybrid", name="hackathonformat")


def upgrade() -> None:
    op.create_table(
        "organizer",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("full_name", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("phone", sa.String(), nullable=False),
        sa.Column("organization", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "participant",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("full_name", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("contact_number", sa.String(), nullable=False),
        sa.Column("specialization", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "hackathon",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("city", sa.String(), nullable=False),
        sa.Column("format", hackathon_format, nullable=False),
        sa.Column("duration_hours", sa.Integer(), nullable=False),
        sa.Column("organizer_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["organizer_id"], ["organizer.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "challengetask",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("requirements", sa.String(), nullable=False),
        sa.Column("evaluation_criteria", sa.String(), nullable=False),
        sa.Column("hackathon_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["hackathon_id"], ["hackathon.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "participanthackathonlink",
        sa.Column("participant_id", sa.Integer(), nullable=False),
        sa.Column("hackathon_id", sa.Integer(), nullable=False),
        sa.Column("role_in_hackathon", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(["hackathon_id"], ["hackathon.id"]),
        sa.ForeignKeyConstraint(["participant_id"], ["participant.id"]),
        sa.PrimaryKeyConstraint("participant_id", "hackathon_id"),
    )
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("full_name", sa.String(), nullable=True),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_user_email"), "user", ["email"], unique=True)
    op.create_index(op.f("ix_user_username"), "user", ["username"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_user_username"), table_name="user")
    op.drop_index(op.f("ix_user_email"), table_name="user")
    op.drop_table("user")
    op.drop_table("participanthackathonlink")
    op.drop_table("challengetask")
    op.drop_table("hackathon")
    op.drop_table("participant")
    op.drop_table("organizer")
    op.execute("DROP TYPE IF EXISTS hackathonformat")
