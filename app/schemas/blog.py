from pydantic import BaseModel
from datetime import datetime
from .user import UserOut

from pydantic.types import conint

class BlogBase(BaseModel):
    title: str
    content: str
    

class BlogCreate(BlogBase):
    pass

class Blog(BlogBase):
    id: int
    date: datetime
    owner_id: int
    author: UserOut

    class Config:
        orm_mode = True

class BlogOut(BaseModel):
    title: str
    content: str
    date: datetime

    class Config:
        orm_mode = True


class Like(BaseModel):
    blog_id: int
    dir: conint(le=1)
