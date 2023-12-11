from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

# Importing models and schemas related to Likes entities
from ..models.models import Likes
from ..schemas.blog import Like

# Importing dependency functions for database access and user authentication
from ..middleware.oauth2 import get_current_user
from ..db.config import get_db

# Creating a FastAPI router for handling Likes-related endpoints
router = APIRouter(
    prefix="/likes",
    tags=['Likes']
)

# Endpoint for adding or removing a like on a blog post
@router.post("/")
def vote(like: Like, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    """
    Add or remove a like on a blog post.
    """
    # Checking if the blog post exists
    blog = db.query(Likes).filter(Likes.id == like.blog_id).first()
    
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Blog with id: {like.blog_id} does not exist")

    # Querying for an existing like by the user on the specified blog post
    like_query = db.query(Likes).filter(
        Likes.blog_id == like.blog_id, Likes.user_id == current_user.id)

    found_like = like_query.first()

    # Adding a like if the direction is positive (1)
    if (like.dir == 1):
        if found_like:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                                detail=f"User {current_user.id} has already liked article {like.blog_id}")
        
        new_like = Likes(blog_id=like.blog_id, user_id=current_user.id)
        db.add(new_like)
        db.commit()

    # Removing a like if the direction is negative (not positive)
    else:
        if not found_like:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Like does not exist")
        
        like_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "Successfully added or removed like"}
