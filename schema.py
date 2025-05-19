from pydantic import BaseModel
from datetime import datetime
class Post(BaseModel):
    title: str
    content: str
    user_id: int
    
    
class ItemRead(BaseModel):
    id: int
    title: str
    content: str
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True
        # orm_mode = True  // this is deprecated so use from_attributes inorder to return the data from the database in an object format
        # from_attributes=True is used to convert the attributes of the model to a dictionary
        
class User(BaseModel):
    username:str
    email:str
    password:str
    
class UserRead(BaseModel):
    id:int
    username:str
    email:str
    password:str

    class Config:
        from_attributes = True
      