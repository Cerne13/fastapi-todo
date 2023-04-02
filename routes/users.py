import sys

from services.auth_service import AuthService

sys.path.append('..')

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from database import get_db
from routes.auth import get_current_user
from schemas.user_schemas import UserVerification, UserResponse
from services.user_services import UserService

router = APIRouter(
    prefix='/users',
    tags=['users'],
    responses={
        404: {'description': 'Not found'}
    }
)

# models.Base.metadata.create_all(bind=engine)


@router.get('/', response_model=list[UserResponse])
async def read_all(db: Session = Depends(get_db)) -> list[UserResponse]:
    user_service = UserService(db=db)
    result = await user_service.get_all_users()
    return result


@router.get('/{user_id}', response_model=UserResponse)
async def get_user_by_id(user_id: int, db: Session = Depends(get_db)) -> UserResponse:
    user_service = UserService(db=db)
    result = await user_service.get_user_by_id(user_id=user_id)
    return result


@router.get('/user/', response_model=UserResponse)
async def get_user_by_query_param_id(user_id: int, db: Session = Depends(get_db)) -> UserResponse:
    user_service = UserService(db=db)
    result = await user_service.get_user_by_query_param_id(user_id=user_id)
    return result


@router.put('/user/password')
async def update_user_password(
        user_verification: UserVerification,
        user: UserResponse = Depends(get_current_user),
        db: Session = Depends(get_db)
) -> str:
    if user is None:
        raise AuthService.get_user_exception()

    user_service = UserService(db=db)
    result = await user_service.update_user_password(user_id=user.id, user_verification=user_verification)
    return result


@router.delete('/user')
async def delete_user(
        user: UserResponse = Depends(get_current_user),
        db: Session = Depends(get_db)
) -> str:
    if user is None:
        raise AuthService.get_user_exception()

    user_service = UserService(db=db)
    result = await user_service.delete_user(user_id=user.id)
    return result
