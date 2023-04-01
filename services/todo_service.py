from typing import Type

from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import Todos
from schemas.todos_schemas import Todo, TodoList


class TodoService:
    def __init__(self, db: Session):
        self.db = db

    @staticmethod
    def successful_response(code: int):
        return {
            'status': code,
            'transaction': 'Successful'
        }

    @staticmethod
    def http_exception_404():
        return HTTPException(status_code=404, detail='Item not found')

    async def get_all_todos(self):
        results = self.db.query(Todos).all()
        return TodoList(
            total=len(results),
            todos=[result.__dict__ for result in results]
        )

    async def get_todos_by_user(self, user_id: int) -> TodoList:
        results = self.db.query(Todos).filter(Todos.user_id == user_id).all()
        return TodoList(
            total=len(results),
            todos=[result.__dict__ for result in results]
        )

    async def get_one_todo(self, todo_id: int, user_id: int) -> Todo:
        todo_model = self.db.query(Todos).filter(Todos.id == todo_id).filter(Todos.user_id == user_id).first()

        if todo_model is not None:
            return Todo(**todo_model.__dict__)
        raise self.http_exception_404()

    async def create_todo(self, todo: Todo, user_id: int):
        todo_model = Todos(
            title=todo.title,
            description=todo.description,
            priority=todo.priority,
            complete=todo.complete,
            user_id=user_id
        )
        self.db.add(todo_model)
        self.db.commit()
        return self.successful_response(201)

    async def update_todo(self, todo_id: int, todo: Todo, user_id: int):
        todo_model = self.db.query(Todos) \
            .filter(Todos.id == todo_id) \
            .filter(Todos.user_id == user_id) \
            .first()

        if todo_model is None:
            raise self.http_exception_404()

        todo_model.title = todo.title
        todo_model.description = todo.description
        todo_model.priority = todo.priority
        todo_model.complete = todo.complete

        self.db.add(todo_model)
        self.db.commit()

        return self.successful_response(200)

    async def delete_todo(self, todo_id: int, user_id: int):
        todo_model = self.db.query(Todos) \
            .filter(Todos.id == todo_id) \
            .filter(Todos.user_id == user_id) \
            .first()

        if todo_model is None:
            raise self.http_exception_404()

        self.db.query(Todos).filter(Todos.id == todo_id).delete()
        self.db.commit()

        return self.successful_response(200)
