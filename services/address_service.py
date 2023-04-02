from sqlalchemy.orm import Session

from models.models import Users, Address
from schemas.address_schemas import AddressSchema
from schemas.user_schemas import UserResponse


class AddressService:
    def __init__(self, db: Session):
        self.db = db

    async def create_address(self, address: AddressSchema, user: UserResponse) -> None:
        address_model = Address(
            address1=address.address1,
            address2=address.address2,
            city=address.city,
            state=address.state,
            country=address.country,
            postal_code=address.postal_code,
            apt_num=address.apt_num
        )

        self.db.add(address_model)
        self.db.flush()

        user_model = self.db.query(Users).filter(Users.id == user.id).first()
        user_model.address_id = address_model.id

        self.db.add(user_model)
        self.db.commit()
