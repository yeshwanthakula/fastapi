from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional
from pydantic import conint
class Post(BaseModel):
    title:str
    content:str
    published:bool = True


# The reason for creating such below classes is ,
#    when sending  the data back from api , we can use inheritance to explicilty send the only needed data .
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True
class CreatePost(Post):
    pass
class ReturPost(BaseModel):
    title:str
    content:str
    id:int
    user_id: int
    created_at : datetime
    user : UserOut

    
    class Config:
        orm_mode = True
# The reason for adding class config orm_mode , 
# is to avoid the ambuigity between orm model and pydantic

class PostOut(BaseModel):
    Post:ReturPost
    votes:int

    class Config:
        orm_mode = True
        
class UserCreate(BaseModel):
    email:EmailStr
    password : str


class UserLogin(BaseModel):
    email:EmailStr
    password : str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None

class votes(BaseModel):
    dir: conint(le=1) # type: ignore
    post_id : int





