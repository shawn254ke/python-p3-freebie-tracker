"""create freebies table

Revision ID: <to-be-filled>
Revises: 5f72c58bf48c
Create Date: <to-be-filled>

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '<to-be-filled>'
down_revision = '5f72c58bf48c'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        'freebies',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('item_name', sa.String(), nullable=False),
        sa.Column('value', sa.Integer(), nullable=False),
        sa.Column('dev_id', sa.Integer(), sa.ForeignKey('devs.id'), nullable=False),
        sa.Column('company_id', sa.Integer(), sa.ForeignKey('companies.id'), nullable=False)
    )

def downgrade() -> None:
    op.drop_table('freebies')
