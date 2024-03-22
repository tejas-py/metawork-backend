from pydantic import BaseModel
from typing import List, Literal, Union


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
    holding: Union[List[HoldingBase], None]
    total_yield: Union[List[TotalYieldBase], None]
    trade_history: Union[List[TradeHistoryBase], None]
    registration_date_time: Union[int, None]
    last_online: Union[int, None]
    total_investments: int
