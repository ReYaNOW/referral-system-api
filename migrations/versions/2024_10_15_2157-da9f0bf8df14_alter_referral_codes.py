"""alter referral_codes

Revision ID: da9f0bf8df14
Revises: fc9fd36532c6
Create Date: 2024-10-15 21:57:13.005958

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'da9f0bf8df14'
down_revision: Union[str, None] = 'fc9fd36532c6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('referral_codes_user_id_fkey', 'referral_codes', type_='foreignkey')
    op.create_foreign_key(None, 'referral_codes', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'referral_codes', type_='foreignkey')
    op.create_foreign_key('referral_codes_user_id_fkey', 'referral_codes', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###
