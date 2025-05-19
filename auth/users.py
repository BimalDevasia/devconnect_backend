from fastapi import APIRouter,Depends
from fastapi import HTTPException
from models import User
from schema import User as UserSchema, UserRead
from typing import List
from sqlalchemy import or_
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db

router = APIRouter()

@router.post("/", response_model=UserRead)
async def create_user(user: UserSchema, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(or_(User.username == user.username, User.email == user.email)))
    existing_user = result.scalar_one_or_none() 
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already exists")
    else:
        
    
    
        new_user = User(**user.model_dump()) # Unpack the user schema into the User model ..Previously use .dict() but now use model_dump()
        try:
            db.add(new_user)
            await db.commit()
            await db.refresh(new_user)
            return new_user
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=400, detail=f"Failed to create user: {e}")