from fastapi import status, HTTPException, Depends, APIRouter, Response
from sqlalchemy.orm import Session

# Importing models and schemas related to Blog entities
from ..models.models import Blog
from ..schemas import blog

# Importing database configuration and dependency functions
from ..db.config import get_db
from ..middleware.oauth2 import get_current_user

# Importing typing for type hints
from typing import List, Optional

# Creating a FastAPI router for handling Blog-related endpoints
router = APIRouter(
    prefix="/blogs",
    tags=['Blogs']
)

# Endpoint for retrieving a list of blogs with optional parameters for pagination and search
@router.get("/", response_model=List[blog.Blog])
def get_blogs(db: Session = Depends(get_db), 
              current_user: int = Depends(get_current_user), 
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    """
    Retrieve a list of blogs with optional pagination and search parameters.
    """
    blogs = db.query(Blog).limit(limit).offset(skip).all()
    return blogs

# Endpoint for creating a new blog post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=blog.BlogOut)
def create_blog(blog: blog.BlogCreate, 
                db: Session = Depends(get_db), 
                current_user: int = Depends(get_current_user)):
    """
    Create a new blog post.
    """
    new_blog = Blog(owner_id=current_user.id, **blog.dict())
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

# Endpoint for retrieving a specific blog post by its ID
@router.get("/{id}", response_model=blog.Blog)
def get_blog(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    """
    Retrieve a specific blog post by its ID.
    """
    try:
        blog = db.query(Blog).group_by(Blog.id).filter(Blog.id == id).first()

        # Validation
        if not blog:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail=f"Blog with id: {id} was not found")
        
        if blog.owner_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                                detail="Not authorized to perform request action")
        
        return blog
    except:
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                        detail=f"Contact with Admin")

# Endpoint for updating a specific blog post by its ID
@router.put("/{id}", response_model=blog.BlogOut, status_code=status.HTTP_200_OK)
def update_blog(id: int, 
                updated_blog: blog.BlogCreate, 
                db: Session = Depends(get_db), 
                current_user: int = Depends(get_current_user)):
    """
    Update a specific blog post by its ID.
    """
    blog_query = db.query(Blog).filter(Blog.id == id)
    blog = blog_query.first()

    # Validation
    if blog is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Blog with id: {id} does not exist")
    
    if blog.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perform request action")
    
    blog_query.update(updated_blog.dict(), synchronize_session=False)
    db.commit()
    return blog_query.first()

# Endpoint for deleting a specific blog post by its ID
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    """
    Delete a specific blog post by its ID.
    """
    blog_query = db.query(Blog).filter(Blog.id == id)
    blog = blog_query.first()

    # Validation
    if blog is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id: {id} does not exist")
    
    if blog.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform request action")
    
    blog_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
