import sys

from schemas.auth_schemas import SignInRequest
from services.auth_service import AuthService, get_current_user_dependency

sys.path.append('..')

from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from database import engine, get_db
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

import models
from schemas.user_schemas import CreateUser, UserResponse

models.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix='/auth',
    tags=['auth'],
    responses={
        401: {'user': 'Not authorized'}
    }
)


@router.post('/create/user')
async def create_new_user(create_user: CreateUser, db: Session = Depends(get_db)):
    service = AuthService(db=db)
    result = await service.create_user(create_user=create_user)
    return result


@router.post('/token')
async def login_for_access_token(
        login: SignInRequest,
        db: Session = Depends(get_db)
):
    service = AuthService(db=db)
    result = await service.login_for_access_token(username=login.username, password=login.password)
    return result


@router.get('/me/', response_model=UserResponse)
async def get_current_user(
        user: UserResponse = Depends(get_current_user_dependency),
) -> UserResponse:
    return user