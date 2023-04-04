import sys

sys.path.append('..')

from fastapi import Depends, APIRouter, Response, Form
from sqlalchemy.orm import Session
from starlette.requests import Request
from fastapi.responses import HTMLResponse
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


@router.get('/current_user/')
async def get_current_user_http(request: Request, db: Session = Depends(get_db)):
    service = AuthService(db=db)
    result = await service.get_current_user_http(request=request)
    return result


# For front
@router.get('/login', response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse('login.html', context={'request': request})


@router.get("/", response_class=HTMLResponse)
async def authentication_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post('/', response_class=HTMLResponse)
async def login_user(request: Request, db: Session = Depends(get_db)):
    service = AuthService(db=db)
    result = await service.login_user(request=request)
    return result


@router.get('/logout', response_class=HTMLResponse)
async def logout(request: Request):
    msg = "Logout successful"
    response = templates.TemplateResponse('login.html', context={'request': request, 'message': msg})
    response.delete_cookie('access_token')
    return response


@router.get('/register', response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse('register.html', context={'request': request})


@router.post('/register', response_class=HTMLResponse)
async def register_user(
        request: Request,
        email: str = Form(...),
        username: str = Form(...),
        first_name: str = Form(...),
        last_name: str = Form(...),
        password: str = Form(...),
        password2: str = Form(...),
        db: Session = Depends(get_db)
):
    user_dict = {
        'email': email,
        'username': username,
        'first_name': first_name,
        'last_name': last_name,
        'password': password,
        'password2': password2
    }
    service = AuthService(db=db)
    result = await service.register_user(request=request, user=user_dict)
    return result
