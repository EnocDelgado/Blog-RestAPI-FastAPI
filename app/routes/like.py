from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..models.models import Likes
from ..schemas.blog import Like
from ..middleware.oauth2 import get_current_user
from ..db.config import get_db


router = APIRouter(
    prefix="/likes",
    tags=['Likes']
)

@router.post("/")
def vote(like: Like, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):

    blog = db.query(Likes).filter(Likes.id == like.blog_id).first()

    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Blog with id: {like.blog_id} does not exist")

    like_query = db.query(Likes).filter(
        Likes.blog_id == like.blog_id, Likes.user_id == current_user.id)

    found_like = like_query.first()

    if (like.dir == 1):
        if found_like:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                            detail=f"user {current_user.id} has already liked on article {like.blog_id}")
    
        new_like = Likes(blog_id=like.blog_id, user_id=current_user.id)
        db.add(new_like)
        db.commit()

    else:
        if not found_like:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Like does not exist")
        
        like_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "Successful added like"}
