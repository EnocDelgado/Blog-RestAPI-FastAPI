from pydantic import BaseModel
from datetime import datetime
from .user import UserOut

# Importing a specific type for integer constraints
from pydantic.types import conint

# Defining a base class for representing the structure of a Blog entity
class BlogBase(BaseModel):
    # Properties for title and content, used for data validation
    title: str
    content: str

# Creating a class for input data when creating a new Blog post, inheriting from BlogBase
class BlogCreate(BlogBase):
    # Inheriting properties from BlogBase, as no additional properties are required for creation
    pass

# Defining a class representing a Blog entity, including additional properties like id, date, owner_id, and author
class Blog(BlogBase):
    id: int            # Unique identifier for the blog post
    date: datetime     # Date and time when the blog post was created
    owner_id: int      # Identifier for the owner of the blog post
    author: UserOut    # Information about the author of the blog post

    # Configuring the class to be used in ORM (Object-Relational Mapping) mode for database operations
    class Config:
        orm_mode = True

# Defining a class for output data representing a simplified view of a Blog entity
class BlogOut(BaseModel):
    title: str         # Title of the blog post
    content: str       # Content of the blog post
    date: datetime     # Date and time when the blog post was created

    # Configuring the class to be used in ORM mode for database operations
    class Config:
        orm_mode = True

# Defining a class for representing the data structure of a "Like" entity
class Like(BaseModel):
    blog_id: int       # Identifier for the blog post being liked
    dir: conint(le=1)  # Integer representing the direction of the like (e.g., +1 for a like)
