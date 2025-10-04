from fastapi import APIRouter, HTTPException, status, Response, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select
from ..database import SessionDep
from ..models.user_models import User, UserLogin
from .. import token_managing as tm

router = APIRouter(
    tags=["Authentication"]

)

from typing import Optional

from fastapi import Body

@router.get("/login", response_model=tm.Token)
def login(session: SessionDep, user_cred: OAuth2PasswordRequestForm = Depends()):
    user = session.exec(select(User).where(User.email == user_cred.username)).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    if not tm.verify_password(user.password, user_cred.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    access_token = tm.create_access_token(data={"user_id": user.id})
    
    return {"access_token": access_token, "token_type": "bearer"}


