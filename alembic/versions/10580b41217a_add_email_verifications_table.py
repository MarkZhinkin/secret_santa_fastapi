"""add email verifications table

Revision ID: 10580b41217a
Revises: be7f75c800cc
Create Date: 2022-03-28 12:08:04.257572

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '10580b41217a'
down_revision = 'be7f75c800cc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('email_verifications',
    sa.Column('id', mysql.BIGINT(unsigned=True), autoincrement=True, nullable=False),
    sa.Column('email', sa.VARCHAR(length=320), nullable=False),
    sa.Column('code', sa.VARCHAR(length=16), nullable=False),
    sa.Column('message_uid', sa.VARCHAR(length=128), nullable=False),
    sa.Column('created_at', mysql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', mysql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('deleted_at', mysql.TIMESTAMP(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_email_verifications_deleted_at'), 'email_verifications', ['deleted_at'], unique=False)
    op.create_index(op.f('ix_email_verifications_email'), 'email_verifications', ['email'], unique=False)
    op.create_index(op.f('ix_email_verifications_message_uid'), 'email_verifications', ['message_uid'], unique=True)
    op.create_index(op.f('ix_email_verifications_updated_at'), 'email_verifications', ['updated_at'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_email_verifications_updated_at'), table_name='email_verifications')
    op.drop_index(op.f('ix_email_verifications_message_uid'), table_name='email_verifications')
    op.drop_index(op.f('ix_email_verifications_email'), table_name='email_verifications')
    op.drop_index(op.f('ix_email_verifications_deleted_at'), table_name='email_verifications')
    op.drop_table('email_verifications')
    # ### end Alembic commands ###
