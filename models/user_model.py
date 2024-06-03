from sqlalchemy import Column, ForeignKey, Integer, String, Enum, Boolean
from connection.database import Base


class Users(Base):
    __tablename__ = 'users'

    auth_id = Column(String, primary_key=True, index=True, unique=True)
    name = Column(String, default="No Name")
    wallet_address = Column(String, index=True, unique=True)
    registration_date_time = Column(Integer)
    last_online = Column(Integer)
    total_investments = Column(Integer)
    dividend_wallet = Column(String, unique=True, nullable=True)
    blocked = Column(Boolean, default=False)
    user_type = Column(Enum("metaworker", "investor", "both", "admin", name="user_type"))


class GenopetsWallet(Base):
    __tablename__ = 'genopets_wallet'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    blockchain = Column(String)
    holding_wallet = Column(String, unique=True)
    user_id = Column(String, ForeignKey("users.auth_id"))


class SynesisOneWallet(Base):
    __tablename__ = 'synesis_one_wallet'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    blockchain = Column(String)
    holding_wallet = Column(String, unique=True)
    user_id = Column(String, ForeignKey("users.auth_id"))


class StarAtlasWallet(Base):
    __tablename__ = 'star_atlas_wallet'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    blockchain = Column(String)
    holding_wallet = Column(String, unique=True)
    user_id = Column(String, ForeignKey("users.auth_id"))


class TradeHistory(Base):
    __tablename__ = 'trade_history'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    asset_name = Column(String)
    amount = Column(Integer)
    price = Column(Integer)
    time = Column(Integer)
    trade_type = Column(Enum("buy", "sell", name="trade_action"))
    user_id = Column(String, ForeignKey("users.auth_id"))
