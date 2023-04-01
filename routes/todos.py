import sys
from typing import Type

from routes.auth import get_current_user
from schemas.user_schemas import UserResponse
from services.todo_service import TodoService

sys.path.append('..')

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from database import engine, get_db
from services.auth_service import AuthService
import models
from schemas.todos_schemas import Todo, TodoList

router = APIRouter(
    prefix='/todos',
    tags=['todos'],
    responses={
        404: {'description': 'Not found'}
    }
)

models.Base.metadata.create_all(bind=engine)


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
