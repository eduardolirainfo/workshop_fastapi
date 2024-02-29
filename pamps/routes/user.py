from typing import List

from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from sqlmodel import Session, select

from pamps.auth import AuthenticatedUser
from pamps.db import ActiveSession
from pamps.models.user import (
    User,
    UserRequest,
    UserResponse,
    SocialResponse,
    SocialRequest,
    Social
)

from pamps.models.post import (
    Post,
    PostResponse,
)

router = APIRouter()


@router.get("/", response_model=List[UserResponse])
async def list_users(*, session: Session = ActiveSession):
    """List all users."""
    users = session.exec(select(User)).all()
    return users


@router.get("/{username}/", response_model=UserResponse)
async def get_user_by_username(
    *, session: Session = ActiveSession, username: str
):
    """Get user by username"""
    query = select(User).where(User.username == username)
    user = session.exec(query).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(*, session: Session = ActiveSession, user: UserRequest):
    """Creates new user"""
    db_user = User.from_orm(user)  # transform UserRequest in User
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.post("/follow/{id}", response_model=SocialResponse, status_code=201)
async def follow_user(
    *,
    session: Session = ActiveSession,
    id: int,
    user: User = AuthenticatedUser,
    social: SocialRequest
):
    """Follow a user if not already following and dont follow yourself"""
    if user.id == id:
        raise HTTPException(status_code=400, detail="Cannot follow yourself")
    query = select(Social).where(Social.from_user_id == user.id, Social.to_user_id == id) 
    social = session.exec(query).first()
    if social:
        raise HTTPException(status_code=400, detail="Already following")
    db_social = Social(from_user_id=user.id, to_user_id=id)
    session.add(db_social)
    session.commit()
    session.refresh(db_social)
    return db_social


@router.delete("/follow/{id}", status_code=204)
async def unfollow_user(*, session: Session = ActiveSession, id: int, user: User = AuthenticatedUser):
    """Unfollow a user if already following"""
    if user.id == id:
        raise HTTPException(status_code=400, detail="Cannot unfollow yourself")
    query = select(Social).where(Social.from_user_id == user.id, Social.to_user_id == id)
    social = session.exec(query).first()
    if not social:
        raise HTTPException(status_code=400, detail="Not following")
    session.delete(social)
    session.commit()
    return None


@router.get("/follow/{id}", response_model=List[UserResponse])
async def get_following(*, session: Session = ActiveSession, id: int):
    """Get users that a user is following"""
    query = select(User).join(Social).where(Social.from_user_id == id)
    users = session.exec(query).all()
    return users


@router.get("/followers/{id}", response_model=List[UserResponse])
async def get_followers(*, session: Session = ActiveSession, id: int):
    """Get users that a user is following"""
    query = select(User).join(Social).where(Social.to_user_id == id)
    users = session.exec(query).all()
    return users


@router.get("/timeline", response_model=List[PostResponse])
async def get_timeline(
    *,
    session: Session = ActiveSession,
    user: User = AuthenticatedUser
):
    """Get all posts of the users that a user is following"""

    followed_users = select(Social.to_user_id).where(Social.from_user_id == user.id)

    posts = session.exec(
        select(Post)
        .join(followed_users.alias(), Post.user_id == followed_users.c.to_user_id)
    ).all()

    return posts
