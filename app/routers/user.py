from fastapi import status, HTTPException, APIRouter

from sqlmodel import select
from ..database import SessionDep
from ..models.user_models import User, UserCreate, UserRead
from ..models.votes_models import Vote

from argon2 import PasswordHasher

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)
ph = PasswordHasher()

@router.get("/", response_model=list[UserRead])
def get_users(session: SessionDep):
    users = session.exec(select(User)).all()

    return users

@router.get("/{id}", response_model=UserRead)
def get_user(id: int, session: SessionDep):
    user = session.get(User, id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} was not found")

    return user

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserRead)
def create_user(user: UserCreate, session: SessionDep):
    user.password = ph.hash(user.password)
    new_user = User.model_validate(user)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user
