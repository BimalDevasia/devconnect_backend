from fastapi import APIRouter, Depends, HTTPException
from models import Post
from schema import Post as PostSchema, ItemRead
from typing import List
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from auth.oauth2 import get_current_user

router = APIRouter()

@router.post("/", response_model=ItemRead)
async def create_post(post: PostSchema, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    new_post = Post(title=post.title, content=post.content, user_id=current_user.id)
    try:
        db.add(new_post)
        await db.commit()
        await db.refresh(new_post)
        return new_post
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to create post: {e}")

@router.get("/", response_model=List[ItemRead])
async def get_posts(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Post))
    posts = result.scalars().all()
    return posts