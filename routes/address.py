import sys

from services.address_service import AddressService

sys.path.append('..')

from models.models import Users
from routes.auth import get_current_user
from schemas.address_schemas import AddressSchema
from schemas.user_schemas import UserResponse

from fastapi import APIRouter, Depends

from models.models import Address
from sqlalchemy.orm import Session

from services.auth_service import AuthService
from database import get_db

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
