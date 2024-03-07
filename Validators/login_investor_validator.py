from pydantic import BaseModel


class LoginInvestor(BaseModel):
    auth_id: str
