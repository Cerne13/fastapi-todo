import sys

from routes.auth import get_current_user
from schemas.user_schemas import UserResponse
from services.todo_service import TodoService

sys.path.append('..')

from fastapi import Depends, APIRouter, Request
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from database import get_db
from services.auth_service import AuthService
from schemas.todos_schemas import Todo, TodoList

router = APIRouter(
    prefix='/todos',
    tags=['todos'],
    responses={
        404: {'description': 'Not found'}
    }
)

templates = Jinja2Templates(directory='templates')


# models.Base.metadata.create_all(bind=engine)


@router.get('/homepage', response_class=HTMLResponse)
async def home_page(request: Request):
    return templates.TemplateResponse('home.html', {'request': request})


@router.get('/add_todo')
async def add_todo_page(request: Request):
    return templates.TemplateResponse('add-todo.html', {'request': request})


@router.get('/edit_todo')
async def add_todo_page(request: Request):
    return templates.TemplateResponse('edit-todo.html', {'request': request})


@router.get('/log_in')
async def login_page(request: Request):
    return templates.TemplateResponse('login.html', {'request': request})


@router.get('/register')
async def login_page(request: Request):
    return templates.TemplateResponse('register.html', {'request': request})


@router.get('/', response_model=TodoList)
async def read_all(db: Session = Depends(get_db)) -> TodoList:
    service = TodoService(db=db)
    result = await service.get_all_todos()
    return result


@router.get('/user', response_model=TodoList)
async def read_all_by_user(
        user: UserResponse = Depends(get_current_user),
        db: Session = Depends(get_db)
) -> TodoList:
    if user is None:
        raise AuthService.get_user_exception()

    service = TodoService(db=db)
    result = await service.get_todos_by_user(user_id=user.id)
    return result


@router.get('/{todo_id}', response_model=Todo)
async def read_one_todo(
        todo_id: int,
        user: UserResponse = Depends(get_current_user),
        db: Session = Depends(get_db)
) -> Todo:
    if user is None:
        raise AuthService.get_user_exception()

    service = TodoService(db=db)
    result = await service.get_one_todo(todo_id=todo_id, user_id=user.id)
    return result


@router.post('/')
async def post_todo(
        todo: Todo,
        user: UserResponse = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    if user is None:
        raise AuthService.get_user_exception()

    service = TodoService(db=db)
    result = await service.create_todo(todo=todo, user_id=user.id)
    return result


@router.put('/{todo_id}')
async def update_todo(
        todo_id: int,
        todo: Todo,
        user: UserResponse = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    if user is None:
        raise AuthService.get_user_exception()

    service = TodoService(db=db)
    result = await service.update_todo(todo_id=todo_id, todo=todo, user_id=user.id)
    return result


@router.delete('/{todo_id}')
async def delete_todo(
        todo_id: int,
        user: UserResponse = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    if user is None:
        raise AuthService.get_user_exception()

    service = TodoService(db=db)
    result = await service.delete_todo(todo_id=todo_id, user_id=user.id)
    return result
