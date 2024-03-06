from pydantic import BaseModel


class LoginInvestor(BaseModel):
    token_id: int
