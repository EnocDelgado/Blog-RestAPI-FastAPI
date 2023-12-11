from ..db.config import get_db
from ..models.models import User
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from ..environment.config import settings
from .validate_jwt import verify_access_token

# Create an OAuth2PasswordBearer instance for handling token retrieval from the 'login' endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# Retrieve security-related configuration settings from the environment config
SECRECT_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

# Dependency function to get the current user based on the provided token and database session
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # Define an HTTPException for unauthorized access
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                          detail=f"Could not validate credentials", 
                                          headers={"WWW-Authenticate": "Bearer"})
    
    # Verify the access token using the validate_jwt module
    token = verify_access_token(token, credentials_exception)

    # Query the database for the user associated with the provided token's user ID
    user = db.query(User).filter(User.id == token.id).first()

    # Return the user
    return user