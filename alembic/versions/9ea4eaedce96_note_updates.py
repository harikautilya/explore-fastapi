"""Note updates

Revision ID: 9ea4eaedce96
Revises: 0948bc030bfa
Create Date: 2025-10-13 17:23:45.314031

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9ea4eaedce96'
down_revision: Union[str, Sequence[str], None] = '0948bc030bfa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
