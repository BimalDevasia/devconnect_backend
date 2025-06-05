from fastapi import APIRouter
from models import Post
from schema import PostCreate
from typing import List
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from schema import ItemRead
from database import get_db
from auth.auth_utils import get_current_user
from models import User

router = APIRouter()

@router.post("/", response_model=ItemRead)
async def create_post(post: PostCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Use the current authenticated user's ID instead of accepting it from the request
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

@router.get("/my-posts", response_model=List[ItemRead])
async def get_my_posts(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get posts created by the current authenticated user"""
    result = await db.execute(select(Post).where(Post.user_id == current_user.id))
    posts = result.scalars().all()
    return posts

@router.get("/{post_id}", response_model=ItemRead)
async def get_post(post_id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific post by ID"""
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.put("/{post_id}", response_model=ItemRead)
async def update_post(post_id: int, post_update: PostCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Update a post (only by the owner)"""
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this post")
    
    try:
        post.title = post_update.title
        post.content = post_update.content
        await db.commit()
        await db.refresh(post)
        return post
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to update post: {e}")

@router.delete("/{post_id}")
async def delete_post(post_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Delete a post (only by the owner)"""
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this post")
    
    try:
        await db.delete(post)
        await db.commit()
        return {"message": "Post deleted successfully"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to delete post: {e}")



