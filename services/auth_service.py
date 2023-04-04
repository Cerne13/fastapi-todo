from datetime import timedelta, datetime
import time
from typing import Optional

from fastapi import Depends, HTTPException, Response, Request
from fastapi.security import HTTPBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from starlette import status
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from database import get_db
from models.models import Users
from schemas.auth_schemas import Token
from schemas.user_schemas import CreateUser, UserResponse

SECRET_KEY = 'asktua34523489ASGWErtjhfksf897'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
bearer = HTTPBearer()
templates = Jinja2Templates(directory='templates')


class LoginForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.username: Optional[str] = None
        self.password: Optional[str] = None

    async def create_oauth_form(self):
        form = await self.request.form()
        self.username = form.get('email')
        self.password = form.get('password')


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
                msg = 'Authorization credentials fail'
                response = templates.TemplateResponse('login.html', context={'request': request, 'message': msg})
                response.delete_cookie('access_token')
                return response
            return {'username': username, 'id': user.id}

        except JWTError:
            raise HTTPException(status_code=404, detail='User not found')

    async def login_user(self, request: Request):
        try:
            form = LoginForm(request=request)
            await form.create_oauth_form()
            response = RedirectResponse(url='/todo_pages', status_code=status.HTTP_302_FOUND)

            validate_user_cookie = await self.login_for_access_token(
                response=response,
                username=form.username,
                password=form.password
            )
            if not validate_user_cookie:
                msg = 'Incorrect user credentials.'
                return templates.TemplateResponse('login.html', context={'request': request, 'message': msg})
            return response
        except HTTPException:
            msg = 'Authentication error happened'
            return templates.TemplateResponse('login.html', context={'request': request, 'message': msg})

    async def register_user(self, request: Request, user: dict):
        validation1 = self.db.query(Users).filter(Users.username == user.get('username')).first()
        validation2 = self.db.query(Users).filter(Users.email == user.get('email')).first()

        if validation1 is not None or validation2 is not None or user.get('password') != user.get('password2'):
            msg = 'Invalid registration request'
            return templates.TemplateResponse('register.html', context={'request': request, 'message': msg})

        user_model = Users()
        user_model.email=user.get('email')
        user_model.username=user.get('username')
        user_model.first_name=user.get('first_name')
        user_model.last_name=user.get('last_name')
        user_model.hashed_password = self.get_password_hash(user.get('password'))
        user_model.is_active = True

        self.db.add(user_model)
        self.db.commit()

        msg = 'User successfully created'
        return templates.TemplateResponse('login.html', context={'request': request, 'message': msg})