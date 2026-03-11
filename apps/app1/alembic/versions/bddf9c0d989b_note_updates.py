"""Note updates

Revision ID: bddf9c0d989b
Revises: 9ea4eaedce96
Create Date: 2025-10-13 17:25:04.358170

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bddf9c0d989b'
down_revision: Union[str, Sequence[str], None] = '9ea4eaedce96'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
