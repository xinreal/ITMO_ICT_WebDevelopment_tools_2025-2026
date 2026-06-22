from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from connection import get_session
from models import User
from schemas import ChangePasswordRequest, Token, UserPublic, UserRegister
from security import (
    authenticate_user,
    create_access_token,
    get_current_active_user,
    get_password_hash,
    verify_password,
)

router = APIRouter(tags=["auth"])


@router.post("/auth/register", response_model=UserPublic)
def register_user(
    user_data: UserRegister,
    session: Session = Depends(get_session),
) -> User:
    existing_username = session.exec(
        select(User).where(User.username == user_data.username)
    ).first()
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already exists")

    existing_email = session.exec(select(User).where(User.email == user_data.email)).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already exists")

    user = User(
        username=user_data.username,
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=get_password_hash(user_data.password),
        is_active=True,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.post("/auth/login", response_model=Token)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
) -> Token:
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.username})
    return Token(access_token=access_token, token_type="bearer")


@router.get("/users/me", response_model=UserPublic)
def read_users_me(current_user: User = Depends(get_current_active_user)) -> User:
    return current_user


@router.get("/users", response_model=list[UserPublic])
def read_users(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
) -> list[User]:
    return list(session.exec(select(User)).all())


@router.post("/users/change-password")
def change_password(
    password_data: ChangePasswordRequest,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
) -> dict[str, str]:
    if not verify_password(password_data.old_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Old password is incorrect")

    current_user.hashed_password = get_password_hash(password_data.new_password)
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    return {"message": "Password changed successfully"}
