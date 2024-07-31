

from database.schema import UserCreate,Generation,ScriptsCreate
from fastapi.encoders import jsonable_encoder
from database.connection import client
import json 

def create_user(user: UserCreate):
    new_user = client["user"].insert_one({"username": user.username, "email": user.email, "created_at": user.created_at, "updated_at": user.updated_at, "plan": user.plan.value, "clerk_id": user.clerk_id, "primary_email_address_id": user.primary_email_address_id})
    inserted_user = client["user"].find_one({"_id": new_user.inserted_id})
    

    return  json.loads(json.dumps(inserted_user, default=str))
def create_generation(data:Generation):
    new_generation = client["generation"].insert_one({"user_id": data.user_id, "cost": data.cost, "created_at": data.created_at, "updated_at": data.updated_at})
    inserted_generation = client["generation"].find_one({"_id": new_generation.inserted_id})

    return inserted_generation


def get_user(id:str):
    user = client["user"].find_one({"_id": id})
    return json.loads(json.dumps(user, default=str))
