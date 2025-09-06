"""create ticket tables

Revision ID: create_ticket_tables
Revises: add_last_login
Create Date: 2024-09-06 23:12:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'create_ticket_tables'
down_revision = 'add_last_login'
branch_labels = None
depends_on = None

def upgrade():
    # Create TicketStatus enum type
    op.execute("""
        CREATE TYPE ticket_status AS ENUM ('open', 'in_progress', 'resolved');
    """)

    # Create TicketPriority enum type
    op.execute("""
        CREATE TYPE ticket_priority AS ENUM ('low', 'medium', 'high');
    """)

    # Create tickets table
    op.create_table(
        'tickets',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=False),
        sa.Column('status', postgresql.ENUM('open', 'in_progress', 'resolved', name='ticket_status'), nullable=False, server_default='open'),
        sa.Column('priority', postgresql.ENUM('low', 'medium', 'high', name='ticket_priority'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('created_by_id', sa.Integer(), nullable=False),
        sa.Column('site_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['created_by_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['site_id'], ['sites.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tickets_id'), 'tickets', ['id'], unique=False)

    # Create ticket_comments table
    op.create_table(
        'ticket_comments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('content', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('ticket_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['ticket_id'], ['tickets.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ticket_comments_id'), 'ticket_comments', ['id'], unique=False)

def downgrade():
    op.drop_index(op.f('ix_ticket_comments_id'), table_name='ticket_comments')
    op.drop_table('ticket_comments')
    op.drop_index(op.f('ix_tickets_id'), table_name='tickets')
    op.drop_table('tickets')
    op.execute('DROP TYPE ticket_status;')
    op.execute('DROP TYPE ticket_priority;')
