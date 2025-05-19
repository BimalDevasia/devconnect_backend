from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from models import User
from schema import UserSchema, UserRead, Token
from database import get_db
from auth.oauth2 import create_access_token
from auth.jwt import verify_password
from typing import Optional

router = APIRouter()

@router.post("/", response_model=UserRead)
async def create_user(user: UserSchema, db: AsyncSession = Depends(get_db)):
    existing_user = await db.execute(select(User).where(User.username == user.username))
    if existing_user.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
    
    new_user = User(**user.model_dump())
    new_user.set_password(user.password)  # Assuming a method to hash the password
    try:
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Failed to create user: {e}")

@router.post("/login", response_model=Token)
async def login(user: UserSchema, db: AsyncSession = Depends(get_db)):
    db_user = await db.execute(select(User).where(User.username == user.username))
    user = db_user.scalar_one_or_none()
    
    if not user or not verify_password(user.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}