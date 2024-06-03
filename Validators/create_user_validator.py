from pydantic import BaseModel
from typing import List, Literal, Union


class UserBase(BaseModel):
    auth_id: str
    wallet_address: str
    dividend_wallet: str
    registration_date_time: Union[int, None]
    last_online: Union[int, None]
    total_investments: int
    user_type: Literal['metaworker', 'investor', 'both']
