from __future__ import annotations

import datetime
import enum

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship


class ConnectionType(enum.Enum):
    DISCORD = 'discord'
    TWITTER = 'twitter'


# declarative base class
Base = declarative_base()


# User
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    pfp_asset_id = Column(Integer, ForeignKey('asset.id'))
    alias = Column(String)

    # Relationships
    pfp = relationship('Asset', back_populates='user', uselist=False)
    social_connection = relationship('SocialConnection', back_populates='user')
    owner = relationship('Owner', back_populates='user')
    galleries = relationship('Gallery', back_populates='user')


class SocialConnection(Base):
    __tablename__ = 'connection'

    id = Column(Integer, primary_key=True, index=True)
    user = Column(Integer, ForeignKey('user.id'))
    connection_id = Column(String)
    connection_type = Column(Enum(ConnectionType))

    # Relationships
    user = relationship('User', back_populates='social_connections')


# Owner/Wallet
class Owner(Base):
    __tablename__ = 'owner'

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String)
    address_type = Column(String)
    user_id = Column(Integer, ForeignKey('user.id'))

    # Relationships
    user = relationship('User', back_populates='owner')


# Asset
class Asset(Base):
    __tablename__ = 'asset'

    id = Column(Integer, primary_key=True, index=True)
    collection_id = Column(Integer, ForeignKey('collection.id'))
    hash = Column(String)
    name = Column(String)
    fingerprint = Column(String)
    # latest_mint_tx_id = Column(Integer, ForeignKey("asset_tx.id"))
    # latest_tx_id = Column(Integer, ForeignKey("asset_tx.id"))
    current_owner_id = Column(Integer, ForeignKey('owner.id'))

    # Relationships
    user = relationship('User', back_populates='pfp_asset')
    owner = relationship('Owner', back_populates='assets')
    collection = relationship('Collection', back_populates='assets')
    galleries = relationship('GalleryAsset', back_populates='asset')

# Collection


class Collection(Base):
    __tablename__ = 'collection'

    id = Column(Integer, primary_key=True, index=True)
    policy_id = Column(String, nullable=False)
    title = Column(String)

    # Relationships
    assets = relationship('Asset', back_populates='collection')


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
