from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey,DateTime, func
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = "posts"
    id=Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, index=True)
    content = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="posts")
    
class User(Base):
    __tablename__ = "users"
    id=Column(Integer, primary_key=True, index=True, autoincrement=True)
    username=Column(String, index=True, unique=True, nullable=False)
    password=Column(String, nullable=False)
    email=Column(String, index=True, unique=True, nullable=False)
    posts=relationship("Post", back_populates="user")
    