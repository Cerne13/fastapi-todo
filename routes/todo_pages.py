import sys

sys.path.append('..')

from fastapi import Depends, APIRouter, Request
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from database import get_db
from services.auth_service import AuthService
from schemas.todos_schemas import Todo, TodoList
from routes.auth import get_current_user
from schemas.user_schemas import UserResponse
from services.todo_service import TodoService

router = APIRouter(
    prefix='/todo_pages',
    tags=['todo_pages'],
    responses={
        404: {'description': 'Not Found'}
    }
)

templates = Jinja2Templates(directory='templates')


@router.get('/', response_class=HTMLResponse)
async def get_all_by_user(request: Request):
    return templates.TemplateResponse('home.html', context={'request': request})


@router.get('/add-todo', response_class=HTMLResponse)
async def add_todo(request: Request):
    return templates.TemplateResponse('add-todo.html', context={'request': request})


@router.get('/edit-todo/{todo_id}', response_class=HTMLResponse)
async def edit_todo(request: Request):
    return templates.TemplateResponse('edit-todo.html', context={'request': request})


@router.get('/login', response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse('login.html', context={'request': request})


@router.get('/register', response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse('register.html', context={'request': request})
