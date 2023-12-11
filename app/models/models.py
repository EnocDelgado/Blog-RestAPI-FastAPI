# Importing necessary modules and classes for defining database models and relationships
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

# Importing the Base class for model inheritance and configuration
from ..db.config import Base

# Defining the User class as a SQLAlchemy model for the "users" table
class User(Base):
    # Setting the table name for the User model
    __tablename__ = "users"

    # Defining columns for the User model with data types and constraints
    # Primary key for user identification
    id = Column(Integer, primary_key=True, nullable=False)  
    # User's full name
    fullname = Column(String, nullable=False)               
    # User's email (unique constraint)
    email = Column(String, nullable=False, unique=True)     
    # User's password
    password = Column(String, nullable=False)               
    # Timestamp for user creation
    created_at = Column(TIMESTAMP(timezone=True),           
                       nullable=False, server_default=text('now()'))

# Defining the Blog class as a SQLAlchemy model for the "blogs" table
class Blog(Base):
    # Setting the table name for the Blog model
    __tablename__ = "blogs"

    # Defining columns for the Blog model with data types and constraints
    # Primary key for blog post identification
    id = Column(Integer, primary_key=True, nullable=False)  
    # Title of the blog post
    title = Column(String, nullable=False)                  
    # Content of the blog post
    content = Column(String, nullable=False)               
    # Timestamp for blog post creation
    date = Column(TIMESTAMP(timezone=True),                 
                  nullable=False, server_default=text('now()'))
    # Foreign key referencing user_id
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)  

    # Establishing a relationship with the User model using the owner_id column
    author = relationship("User")

# Defining the Likes class as a SQLAlchemy model for the "likes" table
class Likes(Base):
    # Setting the table name for the Likes model
    __tablename__ = "likes"

    # Defining columns for the Likes model with data types and constraints
    # Composite primary key with user_id
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)  
    # Composite primary key with blog_id
    blog_id = Column(Integer, ForeignKey("blogs.id", ondelete="CASCADE"), primary_key=True)  
