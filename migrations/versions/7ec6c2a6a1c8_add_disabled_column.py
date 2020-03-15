"""add disabled column

Revision ID: 7ec6c2a6a1c8
Revises: 9e59e0b9d1cf
Create Date: 2020-02-28 16:12:35.548279

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '7ec6c2a6a1c8'
down_revision = '9e59e0b9d1cf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('flicket_config', 'change_category',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.BOOLEAN(),
               existing_nullable=True)
    op.alter_column('flicket_config', 'change_category_only_admin_or_super_user',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.BOOLEAN(),
               existing_nullable=True)
    op.alter_column('flicket_config', 'mail_ascii_attachments',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.BOOLEAN(),
               existing_nullable=True)
    op.alter_column('flicket_config', 'mail_debug',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.BOOLEAN(),
               existing_nullable=True)
    op.alter_column('flicket_config', 'mail_suppress_send',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.BOOLEAN(),
               existing_nullable=True)
    op.alter_column('flicket_config', 'mail_use_ssl',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.BOOLEAN(),
               existing_nullable=True)
    op.alter_column('flicket_config', 'mail_use_tls',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.BOOLEAN(),
               existing_nullable=True)
    op.alter_column('flicket_config', 'use_auth_domain',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.BOOLEAN(),
               existing_nullable=True)
    op.add_column('flicket_users', sa.Column('disabled', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('flicket_users', 'disabled')
    op.alter_column('flicket_config', 'use_auth_domain',
               existing_type=sa.BOOLEAN(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=True)
    op.alter_column('flicket_config', 'mail_use_tls',
               existing_type=sa.BOOLEAN(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=True)
    op.alter_column('flicket_config', 'mail_use_ssl',
               existing_type=sa.BOOLEAN(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=True)
    op.alter_column('flicket_config', 'mail_suppress_send',
               existing_type=sa.BOOLEAN(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=True)
    op.alter_column('flicket_config', 'mail_debug',
               existing_type=sa.BOOLEAN(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=True)
    op.alter_column('flicket_config', 'mail_ascii_attachments',
               existing_type=sa.BOOLEAN(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=True)
    op.alter_column('flicket_config', 'change_category_only_admin_or_super_user',
               existing_type=sa.BOOLEAN(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=True)
    op.alter_column('flicket_config', 'change_category',
               existing_type=sa.BOOLEAN(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=True)
    # ### end Alembic commands ###
