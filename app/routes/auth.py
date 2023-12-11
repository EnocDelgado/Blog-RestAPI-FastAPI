from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

# Import database-related modules and functions
from ..db.config import get_db
from ..schemas.user import Token
from ..models.models import User 

# Import utility functions and JWT token generation function
from ..helpers import utils
from ..helpers.generate_jwt import create_access_token
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

# Create an instance of APIRouter for authentication-related routes
router = APIRouter(tags=['Authentication'])

# Define a route for handling user login and issuing access tokens
@router.post('/login', response_model=Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    # Query the database to retrieve a user with the provided email
    user = db.query(User).filter(
        User.email == user_credentials.username).first()

    # Validation: Check if the user exists and verify the password
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials")
    
    # Create an access token using the user's ID
    access_token = create_access_token(data={"user_id": user.id})
    
    # Return the generated access token along with its type
    return {"access_token": access_token, "token_type": "bearer"}