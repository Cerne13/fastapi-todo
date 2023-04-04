from datetime import timedelta, datetime
import time
from typing import Optional

from fastapi import Depends, HTTPException, Response, Request
from fastapi.security import HTTPBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from starlette import status

from database import get_db
from models.models import Users
from schemas.auth_schemas import Token
from schemas.user_schemas import CreateUser, UserResponse

SECRET_KEY = 'asktua34523489ASGWErtjhfksf897'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
bearer = HTTPBearer()


async def get_current_user_dependency(
        token: str = Depends(bearer),
        db: Session = Depends(get_db)
) -> UserResponse:
    auth_service = AuthService(db=db)
    user_response = await auth_service.get_current_user(token=token)
    return user_response


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.secret = SECRET_KEY
        self.algorithm = ALGORITHM

    @staticmethod
    def get_password_hash(password):
        return bcrypt_context.hash(password)

    @staticmethod
    def verify_password(plain_pass: str, hashed_pass: str) -> bool:
        return bcrypt_context.verify(plain_pass, hashed_pass)

    def authenticate_user(self, username: str, password: str):
        user = self.db.query(Users).filter_by(username=username).first()

        if not user or not self.verify_password(password, user.hashed_password):
            raise self.get_user_exception()
        return Token(
            access_token=self.create_access_token(username=username),
            token_type='Bearer'
        )

    @staticmethod
    def create_access_token(
            username: str,
            expires_delta: Optional[timedelta] = None
    ):
        encode = {"sub": username}

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=20)
        encode.update({"exp": expire})

        return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def get_user_exception():
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={"WWW-Authenticate": "Bearer"}
        )
        return credentials_exception

    @staticmethod
    def token_exception():
        token_exception_resp = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={"WWW-Authenticate": "Bearer"}
        )
        return token_exception_resp

    def decode_access_token(self, token: str) -> dict:
        try:
            decoded_token = jwt.decode(
                token, self.secret, algorithms=[self.algorithm])
            return decoded_token if decoded_token["exp"] >= int(time.time()) else None
        except:
            return {}

    def get_username_from_token(self, token: Optional[str] = Depends(bearer)) -> str:
        jwt_token = token.credentials
        payload = self.decode_access_token(jwt_token)
        return payload.get('sub')

    # Main methods
    async def create_user(self, create_user: CreateUser):
        create_user_model = Users(
            username=create_user.username,
            email=create_user.email,
            first_name=create_user.first_name,
            last_name=create_user.last_name,
            hashed_password=self.get_password_hash(create_user.password),
            is_active=True,
            phone_number=create_user.phone_number
        )

        self.db.add(create_user_model)
        self.db.commit()

        return {'status': 'Success'}

    async def login_for_access_token(self, response: Response, username: str, password: str) -> bool:
        user = self.authenticate_user(username=username, password=password)
        if not user:
            return False

        token_expires = timedelta(minutes=60)
        token = self.create_access_token(
            username=username,
            expires_delta=token_expires
        )
        response.set_cookie(key='access_token', value=token, httponly=True)
        return True

    async def get_current_user(self, token: Optional[str] = Depends(bearer)) -> UserResponse:
        try:
            username = self.get_username_from_token(token=token)
            if not username:
                raise self.get_user_exception()

            user = self.db.query(Users).filter(
                Users.username == username).first()
            if not user:
                raise self.get_user_exception()

            return UserResponse(**user.__dict__)

        except JWTError:
            raise self.get_user_exception()

    # For front
    async def get_current_user_http(self, request: Request):
        try:
            token = request.cookies.get("access_token")
            if token is None:
                return None
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get('sub')
            user = self.db.query(Users).filter(Users.username == username).first()

            if not username:
                return None
            return {'username': username, 'id': user.id}

        except JWTError:
            raise AuthService.get_user_exception()
