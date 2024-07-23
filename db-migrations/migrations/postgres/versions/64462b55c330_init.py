"""init

Revision ID: 64462b55c330
Revises:
Create Date: 2024-06-24 20:11:44.677931

"""

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = "64462b55c330"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "user",
        sa.Column("user_id", sa.INTEGER(), nullable=False),
        sa.Column("user_name", sa.String(length=256), nullable=True),
        sa.Column("phone_number", sa.String(length=64), nullable=False),
        sa.Column("phone_number_id", sa.String(length=128), nullable=False),
        sa.PrimaryKeyConstraint("user_id"),
        schema="webhook",
    )
    op.create_table(
        "session",
        sa.Column("session_id", sa.INTEGER(), nullable=False),
        sa.Column("user_id", sa.INTEGER(), nullable=True),
        sa.Column("start_time", sa.DateTime(), nullable=True),
        sa.Column("end_time", sa.DateTime(), nullable=True),
        sa.Column(
            "is_archived", sa.Boolean(), server_default=sa.text("false"), nullable=True
        ),
        sa.Column("communication_channel", sa.String(length=32), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["webhook.user.user_id"],
        ),
        sa.PrimaryKeyConstraint("session_id"),
        schema="webhook",
    )
    op.create_table(
        "message",
        sa.Column("message_id", sa.INTEGER(), nullable=False),
        sa.Column("session_id", sa.INTEGER(), nullable=False),
        sa.Column("received_timestamp", sa.DateTime(), nullable=False),
        sa.Column("replied_timestamp", sa.DateTime(), nullable=True),
        sa.Column("user_message", sa.String(length=4096), nullable=True),
        sa.Column("bot_message", sa.String(length=4096), nullable=True),
        sa.Column("wa_message_id", sa.String(length=256), nullable=True),
        sa.Column("concatenated_message_id", sa.INTEGER()),
        sa.ForeignKeyConstraint(
            ["session_id"],
            ["webhook.session.session_id"],
        ),
        sa.PrimaryKeyConstraint("message_id"),
        schema="webhook",
    )
    op.create_table(
        "gpt_response",
        sa.Column("response_id", sa.INTEGER(), nullable=False),
        sa.Column("message_id", sa.INTEGER(), nullable=False),
        sa.Column("prompt", sa.TEXT(), nullable=True),
        sa.ForeignKeyConstraint(
            ["message_id"],
            ["webhook.message.message_id"],
        ),
        sa.PrimaryKeyConstraint("response_id"),
        schema="webhook",
    )
    op.create_table(
        "message_processing",
        sa.Column("message_processing_id", sa.INTEGER(), nullable=False),
        sa.Column("session_id", sa.INTEGER(), nullable=False),
        sa.Column("message_id", sa.INTEGER(), nullable=False),
        sa.ForeignKeyConstraint(
            ["message_id"],
            ["webhook.message.message_id"],
        ),
        sa.ForeignKeyConstraint(
            ["session_id"],
            ["webhook.session.session_id"],
        ),
        sa.PrimaryKeyConstraint("message_processing_id"),
        schema="webhook",
    )
    op.create_table(
        "message_status",
        sa.Column("status_id", sa.INTEGER(), nullable=False),
        sa.Column("message_id", sa.INTEGER(), nullable=False),
        sa.Column("status", sa.String(length=4096), nullable=True),
        sa.Column("timestamp", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["message_id"],
            ["webhook.message.message_id"],
        ),
        sa.PrimaryKeyConstraint("status_id"),
        schema="webhook",
    )


def downgrade() -> None:
    op.drop_table("message_status", schema="webhook")
    op.drop_table("message_processing", schema="webhook")
    op.drop_table("gpt_response", schema="webhook")
    op.drop_table("message", schema="webhook")
    op.drop_table("session", schema="webhook")
    op.drop_table("user", schema="webhook")
