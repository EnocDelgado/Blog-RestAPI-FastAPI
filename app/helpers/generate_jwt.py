from jose import jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer

# Import configuration settings from the environment config module
from ..environment.config import settings

# Create an OAuth2PasswordBearer instance for handling token retrieval from the 'login' endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# Retrieve security-related configuration settings from the environment config
SECRECT_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

# Function to create an access token using the provided data
def create_access_token(data: dict):
    # Copy the data to be encoded
    to_encode = data.copy()

    # Calculate the token expiration time
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    # Encode the JWT (JSON Web Token) using the specified secret key and algorithm
    encoded_jwt = jwt.encode(to_encode, SECRECT_KEY, algorithm=ALGORITHM)

    # Return the encoded JWT as the access token
    return encoded_jwt