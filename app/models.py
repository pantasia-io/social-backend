from __future__ import annotations

import datetime
import enum

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import Numeric
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

convention = {
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(constraint_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s',
}

metadata = MetaData(naming_convention=convention)

# declarative base class
Base = declarative_base(metadata=metadata)


class ConnectionType(enum.Enum):
    DISCORD = 'discord'
    TWITTER = 'twitter'


# User
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    pfp_asset_id = Column(
        Integer, ForeignKey(
            'asset.id', use_alter=True,
        ), nullable=True,
    )
    alias = Column(String)
    datetime_created = Column(DateTime, default=datetime.datetime.now())

    # Relationships
    pfp = relationship('Asset', back_populates='user', uselist=False)
    social_connections = relationship('SocialConnection', back_populates='user')
    wallet = relationship('Wallet', back_populates='user')
    galleries = relationship('Gallery', back_populates='user')


class SocialConnection(Base):
    __tablename__ = 'connection'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    connection_id = Column(String)
    connection_type = Column(Enum(ConnectionType))

    # Relationships
    user = relationship('User', back_populates='social_connections')


# Wallet
class Wallet(Base):
    __tablename__ = 'wallet'

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, index=True)
    address_type = Column(String)
    user_id = Column(Integer, ForeignKey('user.id'))

    # Relationships
    user = relationship('User', back_populates='wallet')
    assets = relationship('Asset', back_populates='wallet')
    asset_txs = relationship('AssetTx', back_populates='wallet')
    asset_mint_txs = relationship('AssetMintTx', back_populates='wallet')

# Collection


class Collection(Base):
    __tablename__ = 'collection'

    id = Column(Integer, primary_key=True, index=True)
    policy_id = Column(String, index=True, nullable=False)
    title = Column(String)

    # Relationships
    assets = relationship('Asset', back_populates='collection')

# Asset


class Asset(Base):
    __tablename__ = 'asset'

    id = Column(Integer, primary_key=True, index=True)
    collection_id = Column(Integer, ForeignKey('collection.id'))
    hash = Column(String)
    name = Column(String)
    fingerprint = Column(String, index=True)

    current_wallet_id = Column(Integer, ForeignKey('wallet.id'))

    # Relationships
    user = relationship('User', back_populates='pfp')
    wallet = relationship('Wallet', back_populates='assets')
    collection = relationship('Collection', back_populates='assets')
    galleries = relationship('GalleryAsset', back_populates='asset')
    asset_txs = relationship('AssetTx', back_populates='asset')
    asset_mint_txs = relationship('AssetMintTx', back_populates='asset')
    asset_ext = relationship('AssetExt', back_populates='asset')


class AssetExt(Base):
    __tablename__ = 'asset_ext'

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey('asset.id'), index=True)
    latest_mint_tx_id = Column(Integer, ForeignKey('asset_mint_tx.id'))
    latest_tx_id = Column(Integer, ForeignKey('asset_tx.id'))

    # Relationships
    asset = relationship('Asset', back_populates='asset_ext')
    asset_latest_txs = relationship('AssetTx', back_populates='asset_ext')
    asset_latest_mint_txs = relationship('AssetMintTx', back_populates='asset_ext')


# Txs


class AssetTx(Base):
    __tablename__ = 'asset_tx'

    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Numeric(20, 0))
    tx_hash = Column(String)
    tx_time = Column(DateTime)
    asset_id = Column(Integer, ForeignKey('asset.id'))
    wallet_id = Column(Integer, ForeignKey('wallet.id'))

    # Relationships
    asset = relationship('Asset', back_populates='asset_txs')
    wallet = relationship('Wallet', back_populates='asset_txs')
    asset_ext = relationship('AssetExt', back_populates='asset_latest_txs')


class AssetMintTx(Base):
    __tablename__ = 'asset_mint_tx'

    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Numeric(20, 0))
    tx_hash = Column(String)
    tx_time = Column(DateTime)
    image = Column(String)
    metadata_ = Column(JSONB, name='metadata')
    files = Column(JSONB)

    asset_id = Column(Integer, ForeignKey('asset.id'))
    wallet_id = Column(Integer, ForeignKey('wallet.id'))

    # Relationships
    asset = relationship('Asset', back_populates='asset_mint_txs')
    wallet = relationship('Wallet', back_populates='asset_mint_txs')
    asset_ext = relationship('AssetExt', back_populates='asset_latest_mint_txs')

# Gallery


class Gallery(Base):
    __tablename__ = 'gallery'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    title = Column(String, default='Favourite')

    # Relationships
    user = relationship('User', back_populates='galleries')
    assets = relationship('GalleryAsset', back_populates='gallery')


class GalleryAsset(Base):
    __tablename__ = 'gallery_asset'

    gallery_id = Column(Integer, ForeignKey('gallery.id'), primary_key=True)
    asset_id = Column(Integer, ForeignKey('asset.id'), primary_key=True)
    datetime_created = Column(DateTime, default=datetime.datetime.now())

    # Relationships
    gallery = relationship('Gallery', back_populates='assets')
    asset = relationship('Asset', back_populates='galleries')
