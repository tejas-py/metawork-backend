from pydantic import BaseModel


class BlockUser(BaseModel):
    auth_id: str
    block: bool
