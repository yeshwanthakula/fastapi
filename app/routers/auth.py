from fastapi import APIRouter,status,Depends,HTTPException
from .. import database , models, schemas,utils,oauth
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated

router = APIRouter(tags = ["Authenticztion"])
# the user_credentials : will do a data type verification ansd depends() will get the data from request body and parse data
@router.post("/login")

def login(user_credentials : OAuth2PasswordRequestForm = Depends(), db : Session = Depends(database.get_db)):
    
    user = db.query(models.Users).filter(models.Users.email == user_credentials.username).first()

    if  not user :
        return HTTPException(status_code= status.HTTP_403_FORBIDDEN , detail= "No user found")
    

    verification = utils.verify_password(user_credentials.password , user.password)

    if not verification:
        return HTTPException(status_code= status.HTTP_403_FORBIDDEN , detail= "Wrong password")
    
    access_token = oauth.create_access_token(data= {"user_id": user.id})


    
    return {"access_token" : access_token , "token_type" : "bearer"}

    