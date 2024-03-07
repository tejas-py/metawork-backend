from sqlalchemy import Column, ForeignKey, Integer, String, Enum, Boolean
from connection.database import Base


class Investors(Base):
    __tablename__ = 'investors'

    auth_id = Column(String, primary_key=True, index=True, unique=True)
    wallet_address = Column(String, index=True, unique=True)
    registration_date_time = Column(Integer)
    last_online = Column(Integer, default=0)
    total_investments = Column(Integer)
    total_withdrawn = Column(Integer)
    blocked = Column(Boolean, default=False)


class Holdings(Base):
    __tablename__ = 'holdings'

    token = Column(String, primary_key=True, index=True, unique=False)
    balance = Column(Integer)
    investors_id = Column(String, ForeignKey("investors.auth_id"))


class TotalYield(Base):
    __tablename__ = 'total_yield'

    amount = Column(Integer, primary_key=True, index=True)
    investors_id = Column(String, ForeignKey("investors.auth_id"))


class TradeHistory(Base):
    __tablename__ = 'trade_history'

    asset_name = Column(String, primary_key=True, index=True)
    amount = Column(Integer)
    price = Column(Integer)
    time = Column(Integer)
    trade_type = Column(Enum("buy", "sell", name="trade_action"))
    investors_id = Column(String, ForeignKey("investors.auth_id"))
