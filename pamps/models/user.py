from datetime import datetime
from typing import Optional, TYPE_CHECKING, List
from sqlmodel import SQLModel, Field, Relationship
from pamps.security import HashedPassword
from pydantic import BaseModel, Extra


if TYPE_CHECKING:
    from pamps.models.post import Post


class User(SQLModel, table=True):
    """Represents a user in the system"""

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(nullable=False, unique=True)
    username: str = Field(nullable=False, unique=True)
    avatar: Optional[str] = None
    bio: Optional[str] = None
    password: HashedPassword

    # it populates the .user attribute on the Content Model
    posts: List["Post"] = Relationship(back_populates="user")


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


class Social(SQLModel, table=True):
    """Represents a social account"""

    id: Optional[int] = Field(default=None, primary_key=True)
    from_user_id: int = Field(nullable=False)
    to_user_id: int = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    class Config:
        extra = Extra.allow
        orm_mode = True
        arbitrary_types_allowed = True
        json_encoders = {bytes: lambda v: v.decode("utf-8")}


class SocialResponse(BaseModel):
    """Serializer for Social Response"""
    from_user_id: Optional[int]
    to_user_id: Optional[int]
    created_at: datetime


class SocialRequest(BaseModel):
    """Serializer for Social request payload"""
    from_user_id: Optional[int]
    to_user_id: Optional[int]
