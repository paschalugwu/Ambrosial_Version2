from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision = '65a1a83e7d72'
down_revision = 'c54b9caea067'
branch_labels = None
depends_on = None

def table_exists(table_name):
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)
    return table_name in inspector.get_table_names()

def upgrade():
    # Check if the table exists before creating it
    if not table_exists('reply'):
        op.create_table('reply',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('content', sa.Text(), nullable=False),
            sa.Column('date_posted', sa.DateTime(), nullable=False),
            sa.Column('user_id', sa.Integer(), nullable=False),
            sa.Column('comment_id', sa.Integer(), nullable=False),
            sa.ForeignKeyConstraint(['comment_id'], ['comment.id'], name='fk_reply_comment_id'),
            sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='fk_reply_user_id'),
            sa.PrimaryKeyConstraint('id')
        )
    
    with op.batch_alter_table('comment', schema=None) as batch_op:
        conn = op.get_bind()
        result = conn.execute(text("PRAGMA foreign_key_list(comment);"))
        constraints = [row[0] for row in result]  # Accessing the first column of each row
        if 'fk_comment_parent_id' in constraints:
            batch_op.drop_constraint('fk_comment_parent_id', type_='foreignkey')
        batch_op.drop_column('parent_id')

    with op.batch_alter_table('reaction', schema=None) as batch_op:
        batch_op.add_column(sa.Column('reply_id', sa.Integer(), nullable=True))
        batch_op.alter_column('comment_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.create_foreign_key('fk_reaction_reply_id', 'reply', ['reply_id'], ['id'])

def downgrade():
    with op.batch_alter_table('reaction', schema=None) as batch_op:
        batch_op.drop_constraint('fk_reaction_reply_id', type_='foreignkey')
        batch_op.alter_column('comment_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.drop_column('reply_id')

    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('parent_id', sa.INTEGER(), nullable=True))
        conn = op.get_bind()
        result = conn.execute(text("PRAGMA foreign_key_list(comment);"))
        constraints = [row[0] for row in result]  # Accessing the first column of each row
        if 'fk_comment_parent_id' not in constraints:
            batch_op.create_foreign_key('fk_comment_parent_id', 'comment', ['parent_id'], ['id'])

    op.drop_table('reply')
