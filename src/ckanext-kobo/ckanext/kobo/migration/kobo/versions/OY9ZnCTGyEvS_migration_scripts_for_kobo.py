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
                "package_id",
                sa.UnicodeText,
                sa.ForeignKey("package.id", deferrable=True),
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
        )


def downgrade():
    op.drop_table("kobo")
