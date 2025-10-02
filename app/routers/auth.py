from fastapi import APIRouter, HTTPException, status, Response
from sqlmodel import select
from ..database import SessionDep
from ..models.user_models import User, UserLogin
from .. import token_managing as tm

router = APIRouter(
    tags=["Authentication"]

)

from typing import Optional

from fastapi import Body

@router.post("/login")
def login(session: SessionDep, user_cred: UserLogin):
    user = session.exec(select(User).where(User.email == user_cred.email)).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")
    
    if not tm.verify_password(user.password, user_cred.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")


    
    return {"token": "token1"}


