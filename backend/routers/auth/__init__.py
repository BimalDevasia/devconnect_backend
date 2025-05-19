# File: /backend/backend/routers/auth/__init__.py

from fastapi import APIRouter

router = APIRouter()

from . import users  # Import the users module to include its routes in the auth router.