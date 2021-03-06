"""Initial Tables

Revision ID: 31713977832b
Revises:
Create Date: 2022-07-29 14:33:09.026098

"""
from __future__ import annotations

import sqlalchemy as sa

from alembic import op


# revision identifiers, used by Alembic.
revision = '31713977832b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'asset',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('hash', sa.String(), nullable=True),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('fingerprint', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_asset')),
    )
    op.create_index(op.f('ix_asset_id'), 'asset', ['id'], unique=False)
    op.create_table(
        'asset_mint_tx',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_asset_mint_tx')),
    )
    op.create_index(op.f('ix_asset_mint_tx_id'), 'asset_mint_tx', ['id'], unique=False)
    op.create_table(
        'asset_tx',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=True),
        sa.Column('tx_hash', sa.String(), nullable=True),
        sa.Column('tx_time', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_asset_tx')),
    )
    op.create_index(op.f('ix_asset_tx_id'), 'asset_tx', ['id'], unique=False)
    op.create_table(
        'collection',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('policy_id', sa.String(), nullable=False),
        sa.Column('title', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_collection')),
    )
    op.create_index(op.f('ix_collection_id'), 'collection', ['id'], unique=False)
    op.create_table(
        'connection',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('connection_id', sa.String(), nullable=True),
        sa.Column(
            'connection_type', sa.Enum(
                'DISCORD', 'TWITTER', name='connectiontype',
            ), nullable=True,
        ),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_connection')),
    )
    op.create_index(op.f('ix_connection_id'), 'connection', ['id'], unique=False)
    op.create_table(
        'gallery',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_gallery')),
    )
    op.create_index(op.f('ix_gallery_id'), 'gallery', ['id'], unique=False)
    op.create_table(
        'user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('alias', sa.String(), nullable=True),
        sa.Column('datetime_created', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_user')),
    )
    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=False)
    op.create_table(
        'wallet',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('address', sa.String(), nullable=True),
        sa.Column('address_type', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_wallet')),
    )
    op.create_index(op.f('ix_wallet_id'), 'wallet', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_wallet_id'), table_name='wallet')
    op.drop_table('wallet')
    op.drop_index(op.f('ix_user_id'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_gallery_id'), table_name='gallery')
    op.drop_table('gallery')
    op.drop_index(op.f('ix_connection_id'), table_name='connection')
    op.drop_table('connection')
    op.drop_index(op.f('ix_collection_id'), table_name='collection')
    op.drop_table('collection')
    op.drop_index(op.f('ix_asset_tx_id'), table_name='asset_tx')
    op.drop_table('asset_tx')
    op.drop_index(op.f('ix_asset_mint_tx_id'), table_name='asset_mint_tx')
    op.drop_table('asset_mint_tx')
    op.drop_index(op.f('ix_asset_id'), table_name='asset')
    op.drop_table('asset')
    # ### end Alembic commands ###
    sa.Enum(name='connectiontype').drop(op.get_bind(), checkfirst=False)
