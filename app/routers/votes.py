from fastapi import FastAPI , Depends ,APIRouter,status,HTTPException
from .. import schemas,models,oauth,database
from sqlalchemy.orm import session


router = APIRouter(prefix = "/votes")

@router.post("/" , status_code=status.HTTP_201_CREATED)
def create_vote(user_vote : schemas.votes , db:session = Depends(database.get_db) , userid : int = Depends(oauth.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == user_vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {user_vote.post_id} does not exist")
    vote_query = db.query(models.Votes).filter(models.Votes.post_id == user_vote.post_id , models.Votes.user_id == userid.id)
    found_vote = vote_query.first()
    if user_vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code= status.HTTP_409_CONFLICT , detail="Already liked the post")
        new_vote = models.Votes(post_id = user_vote.post_id , user_id = userid.id)
        db.add(new_vote)
        db.commit()
        return {"message" : "Post liked succesfully"}
    else:
        if not found_vote:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , detail= "Did not like the post")
        vote_query.delete(synchronize_session = False)
        db.commit()
        return  {"message" : "Like deleted sucesfully"}


    
    
