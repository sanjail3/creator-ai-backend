

from database.schema import UserCreate,Generation,ScriptsCreate
from fastapi.encoders import jsonable_encoder
from database.connection import client
import json 

def create_user(user: UserCreate):
    new_user = client["user"].insert_one({"username": user.username, "email": user.email, "created_at": user.created_at, "updated_at": user.updated_at, "plan": user.plan.value})
    inserted_user = client["user"].find_one({"_id": new_user.inserted_id})
    

    return  json.loads(json.dumps(inserted_user, default=str))
def create_generation(data:Generation):
    new_generation = client["generation"].insert_one({"user_id": data.user_id, "cost": data.cost, "created_at": data.created_at, "updated_at": data.updated_at})
    inserted_generation = client["generation"].find_one({"_id": new_generation.inserted_id})

    return inserted_generation


def get_user(id:str):
    user = client["user"].find_one({"_id": id})
    return json.loads(json.dumps(user, default=str))

def get_generation(id:str):
    generation = client["generation"].find_one({"_id": id})
    return json.loads(json.dumps(generation, default=str))

def get_all_users():
    users = client["user"].find()
    return json.loads(json.dumps(users, default=str))

def get_all_generations():
    generations = client["generation"].find()
    return json.loads(json.dumps(generations, default=str))

def createScripts(script:ScriptsCreate):
    new_scripts = client["scripts"].insert_one({"script": script.script, "created_at": script.created_at, "updated_at": script.updated_at, "generation_id": script.generation_id})

    inserted_scripts = client["scripts"].find_one({"_id": new_scripts.inserted_id})
    return json.loads(json.dumps(inserted_scripts, default=str))


def get_scripts(id:str):
    scripts = client["scripts"].find_one({"_id": id})
    return json.loads(json.dumps(scripts, default=str))

