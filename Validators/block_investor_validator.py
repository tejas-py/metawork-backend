from pydantic import BaseModel


class BlockInvestor(BaseModel):
    token_id: int
    block: bool
