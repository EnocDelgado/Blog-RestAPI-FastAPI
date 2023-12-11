from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..models.models import Blog
from ..schemas import blog
from ..db.config import get_db
from ..middleware.oauth2 import get_current_user
from typing import  List, Optional

router = APIRouter(
    prefix="/blogs",
    tags=['Blogs']
)

@router.get("/", response_model=List[blog.Blog])
def get_blogs(db: Session = Depends(get_db), 
              current_user: int = Depends(get_current_user), 
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    

    blog = db.query(Blog).limit(limit).offset(skip).all()

    return blog


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=blog.BlogOut)
def create_blog(blog: blog.BlogCreate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):

    new_blog = Blog(owner_id=current_user.id, **blog.dict())
    # add blog to our database
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog


@router.get("/{id}", response_model=blog.Blog)
def get_blog(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):

    try:
        blog = db.query(Blog).group_by(
                Blog.id).filter(Blog.id == id).first()

        # Validation
        if not blog:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail=f"Blog with id: {id} was not found")
        
        if blog.owner_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                                detail="Not authorized to perform request action")
        
        return blog
    except:
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Conctact with Admin")


@router.put("/{id}", response_model=blog.BlogOut, status_code=status.HTTP_200_OK)
def update_blog(id: int, updated_blog: blog.BlogCreate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):

    blog_query = db.query(Blog).filter(Blog.id == id)

    blog = blog_query.first()

    # Validation
    if blog == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Blog with id: {id} does not exist")
    
    if blog.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perform request action")
    
    blog_query.update(updated_blog.dict(), synchronize_session=False)

    db.commit()

    return blog_query.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):

    blog_query  = db.query(Blog).filter(Blog.id == id)

    blog = blog_query.first()

    # Validation
    if blog == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Blog with id: {id} does not exists")
    
    if blog.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perform request action")
    
    blog_query .delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT, detail=f"Blog with id: {id} has been deleted")
