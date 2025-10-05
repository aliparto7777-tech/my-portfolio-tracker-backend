from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .db import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    accounts = relationship('Account', back_populates='owner')
    transactions = relationship('Transaction', back_populates='owner')

class Account(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    name = Column(String, nullable=False)
    platform = Column(String, nullable=True)
    type = Column(String, nullable=True)
    manual_balance = Column(Float, default=0.0)
    manual_override = Column(Boolean, default=True)
    currency = Column(String, default='USD')
    update_mode = Column(String, default='manual')
    last_updated = Column(DateTime(timezone=True), server_default=func.now())
    notes = Column(Text, nullable=True)

    owner = relationship('User', back_populates='accounts')
    transactions = relationship('Transaction', back_populates='account', cascade='all, delete-orphan')

class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    account_id = Column(Integer, ForeignKey('accounts.id', ondelete='CASCADE'))
    tx_type = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String, default='USD')
    description = Column(Text, nullable=True)
    ts = Column(Integer, nullable=False)

    owner = relationship('User', back_populates='transactions')
    account = relationship('Account', back_populates='transactions')
