import sys

sys.path.append('..')

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from routes.auth import get_current_user
from schemas.address_schemas import AddressSchema
from schemas.user_schemas import UserResponse
from services.auth_service import AuthService
from services.address_service import AddressService

router = APIRouter(
    prefix='/address',
    tags=['address'],
    responses={
        404: {'description': 'Not found'}
    }
)


@router.post('/')
async def create_address(
        address: AddressSchema,
        user: UserResponse = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    if user is None:
        raise AuthService.get_user_exception()

    service = AddressService(db=db)
    await service.create_address(address=address, user=user)
