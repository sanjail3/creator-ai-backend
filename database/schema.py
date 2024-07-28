from pydantic import BaseModel,Field
from datetime import datetime
from enum import Enum
import uuid

class planEnum(Enum):
    """
    Available plans for the user: 
    """
    FREE = "free"
    PREMIUM = "premium"
class UserCreate(BaseModel):
    username:str
    email:str
    created_at:datetime = datetime.now()
    updated_at:datetime = datetime.now()
    plan : planEnum = planEnum.FREE

    class config:
        allow_population_by_field_name = True

class User(UserCreate):
    id:uuid.UUID
    class Config:
        orm_mode = True
        allow_population_by_field_name = True
