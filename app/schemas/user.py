from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# Define a Pydantic model for creating new users
class UserCreate(BaseModel):
    fullname: str
    email: EmailStr
    password: str

# Define a Pydantic model for updating user information
class UserUpdate(BaseModel):
    fullname: str
    email: EmailStr

# Define a Pydantic model for displaying user details
class UserOut(BaseModel):
    id: int
    fullname: str
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True  # Enables ORM mode for better compatibility with SQLAlchemy

# Define a Pydantic model for user login information
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Define a Pydantic model for the token received upon successful login
class Token(BaseModel):
    access_token: str
    token_type: str

# Define a Pydantic model for token data, including an optional user ID
class TokenData(BaseModel):
    id: Optional[str] = None