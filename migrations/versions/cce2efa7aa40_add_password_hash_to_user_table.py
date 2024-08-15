from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'cce2efa7aa40'
down_revision = 'ba1b110f5166'
branch_labels = None
depends_on = None

def upgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        # Add the column with a default value
        batch_op.add_column(sa.Column('password_hash', sa.String(length=128), nullable=False, server_default='default_hash'))
    
    # Update existing rows to have a non-null value
    op.execute('UPDATE user SET password_hash = "default_hash" WHERE password_hash IS NULL')
    
    with op.batch_alter_table('user', schema=None) as batch_op:
        # Remove the server_default after setting the default value
        batch_op.alter_column('password_hash', server_default=None)

def downgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('password_hash')
