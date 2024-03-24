from .. import models,schemas,utils
from sqlalchemy.orm import Session
from fastapi import FastAPI,requests,Depends,HTTPException,status,APIRouter
from typing import List
from ..database import engine ,SessionLocal,get_db


router = APIRouter()

@router.post("/users" , status_code= status.HTTP_201_CREATED ,response_model= schemas.UserOut)
async def create_user( post : schemas.UserCreate , db: Session = Depends(get_db )):
  
    hashed_password = utils.hash(post.password)
    post.password = hashed_password

    new_user = models.Users(**post.model_dump())

    db.add(new_user)
    db.commit()
    print(new_user)
    db.refresh(new_user)
    return  new_user

@router.get("/users/{id}" ,response_model= schemas.UserOut)
def get_user(id : int ,  db: Session = Depends(get_db )):

    user_details = db.query(models.Users).filter(models.Users.id == id).first()

    if user_details is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND ,detail=f"The user with id {id}, doesnot exist")
    return user_details

