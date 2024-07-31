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
    credits : int = 10
    clerk_id:str
    primary_email_address_id:str

    class config:
        populate_by_name = True

class socialMedia(Enum):
    youtube = "youtube"
    facebook = "facebook"
    instagram = "instagram"
    twitter = "twitter"

class socialMediaDetails(BaseModel):
    platform : socialMedia
    username : str
    userid : str
    
class User(UserCreate):
    id:uuid.UUID
    class Config:
        populate_by_name = True

class Generation(BaseModel):
    user_id : uuid.UUID
    cost : int = 0
    created_at:datetime = datetime.now()
    updated_at:datetime = datetime.now()
class ScriptsCreate(BaseModel):
    script:str
    created_at:datetime = datetime.now()
    updated_at:datetime = datetime.now()
    generation_id:uuid.UUID
    class Config:
        orm_mode = True
        populate_by_name = True
class Generationinput(BaseModel):
    topic:str
    duration:int
    tone:str
    generation_id:uuid.UUID
    
class VideoGeneration(BaseModel):
    generation_id:uuid.UUID
    video_url:str 
    created_at:datetime = datetime.now()
    updated_at:datetime = datetime.now()
    class Config:
        orm_mode = True
        populate_by_name = True