from typing import Optional

from pydantic import BaseModel


class CreateUser(BaseModel):
    name : str
    email : str

class ResponseUser(CreateUser):
    user_id : int
    is_active : bool = True

class UpdateUser(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None