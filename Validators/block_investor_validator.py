from pydantic import BaseModel


class BlockInvestor(BaseModel):
    auth_id: str
    block: bool
