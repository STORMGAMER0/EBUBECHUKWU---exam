from datetime import datetime, date

from pydantic import BaseModel


class RegisterUser(BaseModel):

    user_id : int
    event_id : int
    registration_date: datetime = date.today()


class ResponseRegistration(RegisterUser):
    registration_id: int
    attended: bool = False

