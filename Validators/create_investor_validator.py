from pydantic import BaseModel
from typing import List, Literal


class HoldingBase(BaseModel):
    token: str
    balance: int


class TotalYieldBase(BaseModel):
    amount: int


class TradeHistoryBase(BaseModel):
    asset_name: str
    amount: int
    price: int
    time: int
    trade_type: Literal['buy', 'sell']


class InvestorBase(BaseModel):
    auth_id: str
    wallet_address: str
    holding: List[HoldingBase]
    total_yield: List[TotalYieldBase]
    trade_history: List[TradeHistoryBase]
    registration_date_time: int
    last_online: int
    total_investments: int
    total_withdrawn: int
