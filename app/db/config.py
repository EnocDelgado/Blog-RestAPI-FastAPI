from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Import database configuration settings from the environment config module
from ..environment.config import settings

# Construct the database URL using settings from the environment config
# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/host_name>/<database_name>'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

# Create a SQLAlchemy engine using the constructed database URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a session factory (SessionLocal) with specific settings for autocommit and autoflush
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for declarative models
Base = declarative_base()

# Function to obtain a database session using a context manager (yielding the session)
def get_db():
    # Create a new session using the SessionLocal factory
    db = SessionLocal()
    try:
        # Yield the session to the calling code
        yield db
    finally:
        # Close the session when the context manager is exited
        db.close()