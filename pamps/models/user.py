from typing import Optional
from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    """Represents a user in the system"""

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(nullable=False, unique=True)
    username: str = Field(nullable=False, unique=True)
    avatar: Optional[str] = None
    bio: Optional[str] = None
    password: str = Field(nullable=False)
