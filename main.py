import uvicorn
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from routers import post
from database import get_db, engine, Base
from database import AsyncSessionLocal
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from models import Post
from auth import users

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("Database tables created successfully")
    except Exception as e:
        print(f"Warning: Could not create tables: {e}")
    yield
    # Shutdown
    await engine.dispose()

app = FastAPI(
    title="DevConnect API", 
    description="A social platform for developers", 
    version="1.0.0",
    lifespan=lifespan
)

origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to DevConnect API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "DevConnect API is running"}

app.include_router(post.router, prefix="/api/posts", tags=["posts"])
app.include_router(users.router, prefix="/api/auth", tags=["auth"])

# async def delete():
#     async with AsyncSessionLocal() as session:
#         # Get all posts with user_id = NULL
#         result = await session.execute(select(Post).where(Post.user_id == None))
#         posts = result.scalars().all()

#         for post in posts:
#             await session.delete(post)
        
#         await session.commit()
#         print(f"Deleted {len(posts)} posts with no user_id.")

if __name__ == "__main__":
    # asyncio.run(delete())
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
    
    

