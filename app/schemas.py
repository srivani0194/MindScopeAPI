from pydantic import BaseModel
from typing import Optional
from datetime import date

# when someone signs up or logs in
class UserCreate(BaseModel):
    username: str
    password: str

# when they log in
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class MoodBase(BaseModel):
    mood: str
    activity: str
    energy: str
    date: Optional[date] 

class MoodCreate(MoodBase):
    pass

class MoodOut(MoodBase):
    id: int

    class Config:
        orm_mode = True



