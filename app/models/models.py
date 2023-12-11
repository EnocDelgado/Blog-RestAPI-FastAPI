from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from ..db.config import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, nullable=False)
    fullname = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), 
                       nullable=False, server_default=text('now()'))
    

class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    date = Column(TIMESTAMP(timezone=True), 
                       nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    author = relationship("User")


class Likes(Base):
    __tablename__ = "likes"
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), primary_key=True)
    blog_id = Column(Integer, ForeignKey(
        "blogs.id", ondelete="CASCADE"), primary_key=True)