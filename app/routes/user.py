from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..models.models import User
from ..schemas import user
from ..db.config import get_db
from ..middleware.oauth2 import get_current_user
from ..helpers import utils

# Create an instance of APIRouter for handling user-related routes
router = APIRouter(
    prefix="/users",
    tags=['Users']
)

# Define a route to create a new user
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=user.UserOut)
def create_user(user: user.UserCreate, db: Session = Depends(get_db)):
    try:
        # Hash the password before storing it in the database
        hashed_password = utils.hash(user.password)
        user.password = hashed_password

        # Create a new user instance with the provided data
        new_user = User(**user.dict())

        # Add the user to the database, commit changes, and refresh
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user
    
    except:
        # Handle the case where a user with the same data already exists
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                            detail=f"User already exists")

# Define a route to retrieve a specific user by ID
@router.get("/{id}", response_model=user.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    # Query the database to retrieve a specific user by ID
    user = db.query(User).filter(User.id == id).first()

    # Validation: Check if the user exists
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"User with id: {id} does not exist")
    
    return user

# Define a route to update a specific user by ID
@router.put("/{id}", response_model=user.UserUpdate, status_code=status.HTTP_200_OK)
def update_user(id: int, updated_user: user.UserUpdate, db: Session = Depends(get_db), 
                current_user: int = Depends(get_current_user)):
    # Query the database to retrieve the user for updating
    user_query = db.query(User).filter(User.id == id)
    user = user_query.first()

    # Validation: Check if the user exists and if the current user is authorized
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist")
    
    if user.id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform request action")
    
    # Update the user with the provided data and commit changes
    user_query.update(updated_user.dict(), synchronize_session=False)
    db.commit()

    return user_query.first()

# Define a route to delete a specific user by ID
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    # Query the database to retrieve the user for deletion
    user_query = db.query(User).filter(User.id == id)
    user = user_query.first()

    # Validation: Check if the user exists and if the current user is authorized
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"User with id: {id} does not exist")
    
    if user.id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perform request action")
    
    # Delete the user from the database, commit changes, and return a success response
    user_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)