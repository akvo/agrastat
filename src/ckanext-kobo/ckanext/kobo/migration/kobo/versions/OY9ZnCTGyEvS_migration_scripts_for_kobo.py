"""Migration scripts for tracking

Revision ID: OY9ZnCTGyEv
Revises:
Create Date: 2025-01-17 19:21:29.449298

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "OY9ZnCTGyEvS"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    engine = op.get_bind()
    inspector = sa.inspect(engine)
    tables = inspector.get_table_names()
    if "kobo" not in tables:
        op.create_table(
            "kobo",
            sa.Column("id", sa.Integer, primary_key=True),
            sa.Column(
                "resource_id",
                sa.UnicodeText,
                sa.ForeignKey("resource.id", deferrable=True),
                nullable=True,
            ),
            sa.Column(
                "export_settings_uid", sa.String(length=255), nullable=True
            ),
            sa.Column("asset_uid", sa.String(length=255), nullable=True),
            sa.Column("kobo_token", sa.String(length=255), nullable=True),
            sa.Column("kf_url", sa.String(length=255), nullable=True),
            sa.Column("next_run", sa.DateTime),
            sa.Column("last_run", sa.DateTime),
            # Added columns
            sa.Column("status", sa.String(50), nullable=True),
            sa.Column("error_message", sa.UnicodeText, nullable=True),
            sa.Column("last_successful_run", sa.DateTime, nullable=True),
            sa.Column("update_frequency", sa.String(50), nullable=True),
        )


def downgrade():
    op.drop_table("kobo")
