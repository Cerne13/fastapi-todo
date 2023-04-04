import sys

sys.path.append('..')

from fastapi import Depends, APIRouter, Response, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from starlette import status
from starlette.requests import Request
from fastapi.responses import HTMLResponse
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from database import get_db
from schemas.user_schemas import CreateUser, UserResponse
from schemas.auth_schemas import SignInRequest
from services.auth_service import AuthService, get_current_user_dependency

router = APIRouter(
    prefix='/auth',
    tags=['auth'],
    responses={
        401: {'user': 'Not authorized'}
    }
)
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


@router.post('/create/user')
async def create_new_user(create_user: CreateUser, db: Session = Depends(get_db)):
    service = AuthService(db=db)
    result = await service.create_user(create_user=create_user)
    return result


@router.post('/token')
async def login_for_access_token(
        response: Response,
        login: SignInRequest,
        db: Session = Depends(get_db)
) -> bool:
    service = AuthService(db=db)
    result = await service.login_for_access_token(
        response=response,
        username=login.username,
        password=login.password
    )
    return result


@router.get('/me/', response_model=UserResponse)
async def get_current_user(
        user: UserResponse = Depends(get_current_user_dependency),
) -> UserResponse:
    return user


# For front
@router.get('/login', response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse('login.html', context={'request': request})


@router.post('/', response_class=HTMLResponse)
async def login_user(request: Request, db: Session = Depends(get_db)):
    try:
        form = LoginForm(request=request)
        await form.create_oauth_form()
        response = RedirectResponse(url='/todo_pages', status_code=status.HTTP_302_FOUND)

        service = AuthService(db=db)
        validate_user_cookie = await service.login_for_access_token(
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

@router.get('/register', response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse('register.html', context={'request': request})
