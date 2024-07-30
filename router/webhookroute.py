from fastapi import APIRouter, HTTPException, status
import database.schema as schemas
import database.operation as op
from validator_collection import validators
from database.webhookSchema import Webhook,ClerkUser
import pprint
import json
router = APIRouter(
    prefix="/webhooks",
    tags=["user"],
    responses={404: {"description": "Not found"}},

)

# username:str
#     email:str
#     created_at:datetime = datetime.now()
#     updated_at:datetime = datetime.now()
#     plan : planEnum = planEnum.FREE
#     clerk_id:str
#     primary_email_address_id:str

def create_user(data:dict):
    
    new_user = schemas.UserCreate(username=data["first_name"] + data["last_name"],email=data["email_addresses"][0]["email_address"],created_at=data["created_at"],updated_at=data["updated_at"],clerk_id=data["id"],primary_email_address_id=data["primary_email_address_id"])
    op.create_user(new_user)

    pass

@router.post("/create",status_code=status.HTTP_200_OK)
def webhook(body: Webhook):
    if body.type == "user.created":
        create_user(json.loads(json.dumps(body.data)))
        pass

    return "hi"
