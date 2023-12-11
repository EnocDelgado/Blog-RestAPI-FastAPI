from jose import JWTError, jwt
from ..schemas import user
from fastapi.security import OAuth2PasswordBearer
from ..environment.config import settings

# Create an OAuth2PasswordBearer instance for handling token retrieval from the 'login' endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# Retrieve security-related configuration settings from the environment config
SECRECT_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

# Function to verify and decode an access token
def verify_access_token(token: str, credentials_exception):
    try:
        # Decode the JWT (JSON Web Token) using the specified secret key and algorithm
        payload = jwt.decode(token, SECRECT_KEY, algorithms=[ALGORITHM])

        # Extract the user_id from the decoded payload
        id: str = payload.get("user_id")

        # Raise an exception if user_id is missing in the payload
        if id is None:
            raise credentials_exception
        
        # Create a TokenData instance with the extracted user_id
        token_data = user.TokenData(id=str(id))

    except JWTError:
        # Raise an exception if there's an error decoding the token
        raise credentials_exception
    
    # Return the TokenData instance
    return token_data