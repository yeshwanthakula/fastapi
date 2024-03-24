from fastapi import FastAPI
from .database import engine 
from . import models
from .routers import post,user,auth,votes
from fastapi.middleware.cors import CORSMiddleware
# from starlette.middleware.cors import CORSMiddleware
# import psycopg2
# from  psycopg2.extras import RealDictCursor

app  = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods = ["*"],
    allow_headers=["*"],
    
)



# the below line will create a database in postgre sql swerver
models.Base.metadata.create_all(bind=engine)



app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(votes.router)



# try :
#     # connecting  the psycopg2 and postgre sql server
#     conn = conn = psycopg2.connect(database = "fastapi" ,host ="localhost" ,user = "postgres" ,password ="Apple@2002", cursor_factory= RealDictCursor)
#     cursor = conn.cursor()
#     print("data base connection was succeful")
# except Exception as error:
#     print("Connection ti database failed")
#     print("Error" , error)


@app.get("/")
async def say_hello():
    return {"Hello world"}










    

    
    