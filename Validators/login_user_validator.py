from pydantic import BaseModel


class LoginUser(BaseModel):
    auth_id: str
