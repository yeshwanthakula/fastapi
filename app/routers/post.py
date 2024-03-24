from .. import models,schemas,utils,oauth
from sqlalchemy.orm import Session
from fastapi import FastAPI,requests,Depends,APIRouter,HTTPException,status
from typing import List,Optional
from ..database import engine ,SessionLocal,get_db

from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
)

@router.get("/" ,response_model= List[schemas.PostOut])
# @router.get("/" )
async def say_hello(db: Session  = Depends(get_db) , limit : int = 2 , skip : int = 0 , search : Optional[str] = "") :


    # posts = cursor.execute("""SELECT * FROM posts""")
    # # The below statement is important to fetch rows , above statement alone wont help
    # posts = cursor.fetchall()
    # print(posts)
    search_lower = search.lower()

#     note : any  time you want to make database changes using  orm , we need to pass 
# (db: Session  = Depends(get_db)) as a path operation in the function

    # posts = db.query(models.Post).filter(models.Post.title.contains(func.lower(search))).limit(limit).offset(skip).all()
    posts = (
        db.query(models.Post)
        .filter(func.lower(models.Post.title).contains(search_lower))
        .limit(limit)
        .offset(skip)
        .all()
    )
    # func is used for aggregation function in sql like count , max etc..
    result = (db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(
        models.Votes, models.Votes.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(func.lower(models.Post.title).contains(search_lower))
        .limit(limit)
        .offset(skip)
        .all())
    return result

@router.post("/" ,response_model= schemas.ReturPost)
async def solve(post : schemas.CreatePost , db: Session  = Depends(get_db) , user_id : int = Depends(oauth.get_current_user)) :

    # this is done to prevent sql injection  so  we should avoid  writing
    #cursor.execute(f"""INSERT INTO  posts (content)  VALUES({post.content})  RETURNING * """  )
    #add extra comma for passing one parameter

    # We write like this --> cursor.execute("""INSERT INTO  posts (content)  VALUES(%s)  RETURNING * """ ,(post.content,) )
    # new_post = cursor.fetchone()
    # conn.commit()


    
    # Instead of writing the below code 

    # new_post = models.Post(title = post.title ,content = post.content , published = post.published)
    # we can write 
    try:
        print(user_id)
        new_post = models.Post(user_id = user_id.id , **post.model_dump())

        db.add(new_post)
        db.commit()
        print(new_post)
        db.refresh(new_post)
        return  new_post
    except Exception as e:
        return e

@router.get("/{id}" ,response_model= schemas.Post)
async def get_id(id: int, db: Session  = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id).first()

    # .all() vs .first() method is once u got the answer, .first() methods stops searching

    if not post:
        return HTTPException(detail="ID not found" ,status_code=404)
    return  post

@router.delete("/{id}")
async def delete_by_id(id:int , db : Session  = Depends(get_db) , current_user : int = Depends(oauth.get_current_user)):
    
    # the below line is only a query
        post_query = db.query(models.Post).filter(models.Post.id == id)
        post = post_query.first()
        print(type(current_user))

        if post == None:
            raise HTTPException(detail="ID not found" ,status_code=status.HTTP_404_NOT_FOUND)
        
        if post.user_id!=current_user.id:
            raise HTTPException(status_code= status.HTTP_403_FORBIDDEN ,detail= "Not allowed to delete")
        
        post_query.delete(synchronize_session = False)
        db.commit()
        return {post}
    


# @app.put("/posts/{id}")
# async def update_post(post : Post , id: int , db : Session  = Depends(get_db)):

#     post_query = db.query(models.Post).filter(models.Post.id == id)

#     if post_query.first() == None:
#         return HTTPException(detail="ID NOT FOUND")
    
#     # post1 = post_query.first()
#     # post1.title = post.title
#     # post1.content = post.content
#     post_query.update(**post.model_dump() , synchronize_session = False)
    
#     db.commit()

#     # Close the database session
#     db.close()
#     # post_query.update(**post.model_dump() , synchronize_session = False)
#     # post_query.update(**post.model_dump(), synchronize_session = False)

#     return {"updated post succefully"}



@router.put("/posts/{id}" , response_model= schemas.ReturPost)
async def update_post(id: int, post: schemas.Post, db: Session = Depends(get_db)):
    # Check if the post with the given id exists
    existing_post = db.query(models.Post).filter(models.Post.id == id).first()
    if not existing_post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Update the post with the new data
    update_data = post.dict(exclude_unset=True)  # Exclude unset values (e.g., None)
    db.query(models.Post).filter(models.Post.id == id).update(update_data)

    # Commit the changes to the database
    db.commit()
    db.refresh(existing_post)  # Refresh the existing_post object with updated data

    # The update() method on a SQLAlchemy query object does not accept keyword arguments directly. 
    # Instead, you should use a dictionary to specify the column-value pairs for the update.

    return {"message": "Post updated successfully"}