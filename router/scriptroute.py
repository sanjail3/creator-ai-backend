
from fastapi import APIRouter, HTTPException, status
import database.schema as schemas
import database.operation as op
from validator_collection import validators


router = APIRouter(
    prefix="/scripts",
    tags=["scripts"],
    responses={404: {"description": "Not found"}},

)

@router.post("/generate_script",status_code=status.HTTP_201_CREATED)
def create_script(script):

    #if doesn't have the  credit then redirect to payment page
    pass 






    