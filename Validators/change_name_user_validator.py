from pydantic import BaseModel


class ChangeNameUser(BaseModel):
    auth_id: str
    name: str
