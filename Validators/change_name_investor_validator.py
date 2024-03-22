from pydantic import BaseModel


class ChangeNameInvestor(BaseModel):
    auth_id: str
    name: str
