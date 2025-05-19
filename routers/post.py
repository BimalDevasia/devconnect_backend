from fastapi import APIRouter
from models import Post
from schema import Post as PostSchema
from typing import List
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from schema import ItemRead
from database import get_db

router = APIRouter()

@router.post("/", response_model=ItemRead)
async def create_post(post: PostSchema,db: AsyncSession = Depends(get_db)):
    new_post = Post(title=post.title, content=post.content, user_id=post.user_id)
    try:
        db.add(new_post)
        await db.commit()
        await db.refresh(new_post)
        return new_post
    except Exception as e:
        await db.rollback()
        return {"error": f"Failed to create post : {e}"}
    
@router.get("/", response_model=List[ItemRead])
async def get_posts(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Post))
    posts = result.scalars().all()
    return posts
    


