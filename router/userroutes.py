from fastapi import APIRouter, HTTPException, status
import database.schema as schemas
import database.operation as op
from validator_collection import validators


router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}},

)


@router.post("/signup",status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate):
    if not validators.email(user.email):
        raise HTTPException(status_code=400, detail="Invalid email")
    users = op.create_user(user)
    
    return users

