from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, Text, UniqueConstraint
from sqlalchemy.orm import relationship
import datetime
import enum
from game_server.configs import Base


class Account(Base):
    __tablename__ = 'accounts'

    account_id = Column(Integer, primary_key=True, autoincrement=True)
    nickname = Column(String(50), nullable=False, unique=True, index=True)
    credits = Column(Float, default=0.0, nullable=False)
    creation_date = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    last_login_date = Column(DateTime, nullable=True)

    # Relationships
    items = relationship("AccountItem", back_populates="account")
    transactions = relationship("Transaction", back_populates="account")

    def __repr__(self):
        return f"<Account(nickname='{self.nickname}', credits={self.credits})>"


class Item(Base):
    __tablename__ = 'items'

    item_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    sell_price = Column(Float, nullable=False)
    image_reference = Column(String(255), nullable=True)

    # Relationships
    account_items = relationship("AccountItem", back_populates="item")
    transactions = relationship("Transaction", back_populates="item")

    def __repr__(self):
        return f"<Item(name='{self.name}', price={self.price})>"


class AccountItem(Base):
    __tablename__ = 'account_items'

    account_item_id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey('accounts.account_id'), nullable=False)
    item_id = Column(Integer, ForeignKey('items.item_id'), nullable=False)
    acquisition_date = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    # Relationships
    account = relationship("Account", back_populates="items")
    item = relationship("Item", back_populates="account_items")

    # Ensure an account can only have one of each item
    __table_args__ = (UniqueConstraint('account_id', 'item_id', name='uix_account_item'),)

    def __repr__(self):
        return f"<AccountItem(account_id={self.account_id}, item_id={self.item_id})>"


class TransactionType(enum.Enum):
    PURCHASE = "purchase"
    SALE = "sale"


class Transaction(Base):
    __tablename__ = 'transactions'

    transaction_id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey('accounts.account_id'), nullable=False)
    item_id = Column(Integer, ForeignKey('items.item_id'), nullable=False)
    transaction_type = Column(Enum(TransactionType), nullable=False)
    amount = Column(Float, nullable=False)
    transaction_date = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    # Relationships
    account = relationship("Account", back_populates="transactions")
    item = relationship("Item", back_populates="transactions")

    def __repr__(self):
        return f"<Transaction(account_id={self.account_id}, item_id={self.item_id}, type='{self.transaction_type}', amount={self.amount})>"


class ServerConfiguration(Base):
    __tablename__ = 'server_configuration'

    config_id = Column(Integer, primary_key=True, autoincrement=True)
    min_login_credits = Column(Float, nullable=False, default=10.0)
    max_login_credits = Column(Float, nullable=False, default=100.0)
    config_key = Column(String(100), nullable=False, unique=True)
    config_value = Column(String(255), nullable=True)

    def __repr__(self):
        return f"<ServerConfiguration(config_key='{self.config_key}', config_value='{self.config_value}')>"