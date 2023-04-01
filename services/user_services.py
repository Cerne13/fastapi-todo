from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import Users
from schemas.user_schemas import UserResponse, UserVerification
from services.auth_service import AuthService


class UserService:
    def __init__(self, db: Session):
        self.db = db

    async def get_all_users(self) -> list[UserResponse]:
        users = self.db.query(Users).all()
        return [UserResponse(**user.__dict__) for user in users]

    async def get_user_by_id(self, user_id: int) -> UserResponse:
        user_model = self.db.query(Users).filter(Users.id == user_id).first()

        if user_model is not None:
            return UserResponse(**user_model.__dict__)
        raise HTTPException(status_code=404, detail='Invalid user id')

    async def get_user_by_query_param_id(self, user_id: int) -> UserResponse:
        user_model = self.db.query(Users).filter(Users.id == user_id).first()

        if user_model is not None:
            return UserResponse(**user_model.__dict__)
        raise HTTPException(status_code=404, detail='Invalid user id')

    async def update_user_password(self, user_id: int, user_verification: UserVerification) -> str:
        user_model = self.db.query(Users).filter(Users.id == user_id).first()

        if user_model is not None:
            if user_verification.username == user_model.username and AuthService.verify_password(
                    user_verification.password,
                    user_model.hashed_password):
                user_model.hashed_password = AuthService.get_password_hash(user_verification.new_password)

                self.db.add(user_model)
                self.db.commit()
                return 'successful'

        return 'invalid user or request'

    async def delete_user(self, user_id: int) -> str:
        user_model = self.db.query(Users).filter(Users.id == user_id).first()

        if user_model is None:
            return 'Invalid user or request'

        self.db.query(Users).filter(Users.id == user_id).delete()
        self.db.commit()

        return 'Delete successful'
