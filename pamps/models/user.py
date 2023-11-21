from typing import Optional
from sqlmodel import SQLModel, Field
from pamps.security import HashedPassword
from pydantic import BaseModel


class User(SQLModel, table=True):
    """Represents a user in the system"""

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(nullable=False, unique=True)
    username: str = Field(nullable=False, unique=True)
    avatar: Optional[str] = None
    bio: Optional[str] = None
    password: HashedPassword


class UserResponse(BaseModel):
    """Serializer for User Response"""

    username: str
    avatar: Optional[str] = None
    bio: Optional[str] = None


class UserRequest(BaseModel):
    """Serializer for User request payload"""

    email: str
    username: str
    password: str
    avatar: Optional[str] = None
    bio: Optional[str] = None