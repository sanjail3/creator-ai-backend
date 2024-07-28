

from database.schema import UserCreate
from fastapi.encoders import jsonable_encoder
from database.connection import client
import json 
def create_user(user: UserCreate):
    new_user = client["user"].insert_one({"username": user.username, "email": user.email, "created_at": user.created_at, "updated_at": user.updated_at, "plan": user.plan.value})
    inserted_user = client["user"].find_one({"_id": new_user.inserted_id})
    

    return  json.loads(json.dumps(inserted_user, default=str))
