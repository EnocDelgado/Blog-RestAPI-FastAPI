from passlib.context import CryptContext

# Create a CryptContext instance for password hashing using the bcrypt scheme
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to hash a password using the configured CryptContext instance
def hash(password: str):
    return pwd_context.hash(password)

# Function to verify a plain password against a hashed password using the configured CryptContext instance
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)