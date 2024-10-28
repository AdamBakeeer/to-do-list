"""non-unique

Revision ID: 5847a1e38a00
Revises: e0b5e019709e
Create Date: 2024-10-28 21:37:52.583223

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5847a1e38a00'
down_revision = 'e0b5e019709e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('assessment', schema=None) as batch_op:
        batch_op.drop_index('ix_assessment_Code')
        batch_op.create_index(batch_op.f('ix_assessment_Code'), ['Code'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('assessment', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_assessment_Code'))
        batch_op.create_index('ix_assessment_Code', ['Code'], unique=1)

    # ### end Alembic commands ###
