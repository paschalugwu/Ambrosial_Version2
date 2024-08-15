from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '28008182ab9a'
down_revision = '31986866a4b1'
branch_labels = None
depends_on = None

def upgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password', sa.String(length=128), nullable=False, server_default='default_password'))
        batch_op.drop_column('password_hash')

def downgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password_hash', sa.String(length=128), nullable=False, server_default='default_password'))
        batch_op.drop_column('password')
    # Remove the default value after adding the column
    op.alter_column('user', 'password_hash', server_default=None)
