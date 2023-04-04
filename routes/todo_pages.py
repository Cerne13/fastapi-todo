import sys

from routes.auth import get_current_user_http

sys.path.append('..')

from fastapi import Depends, APIRouter, Request, Form
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from starlette import status

from database import get_db
from models.models import Todos

router = APIRouter(
    prefix='/todo_pages',
    tags=['todo_pages'],
    responses={
        404: {'description': 'Not Found'}
    }
)

templates = Jinja2Templates(directory='templates')


@router.get('/', response_class=HTMLResponse)
async def get_all_by_user(request: Request, db: Session = Depends(get_db)):
    user = await get_current_user_http(request=request, db=db)
    if user is None:
        return RedirectResponse('/auth', status_code=status.HTTP_302_FOUND)

    todos = db.query(Todos).filter(Todos.user_id == user.get('id')).all()

    return templates.TemplateResponse('home.html', context={'request': request, 'todos': todos})


@router.get('/add-todo', response_class=HTMLResponse)
async def add_todo(request: Request, db: Session = Depends(get_db)):
    user = await get_current_user_http(request=request, db=db)
    if user is None:
        return RedirectResponse('/auth', status_code=status.HTTP_302_FOUND)

    return templates.TemplateResponse('add-todo.html', context={'request': request})


@router.post('/add-todo', response_class=HTMLResponse)
async def create_todo(
        request: Request,
        title: str = Form(...),
        description: str = Form(...),
        priority: int = Form(...),
        db: Session = Depends(get_db)
):
    user = await get_current_user_http(request=request, db=db)
    if user is None:
        return RedirectResponse('/auth', status_code=status.HTTP_302_FOUND)

    todo_model = Todos(
        title=title,
        description=description,
        priority=priority,
        complete=False,
        user_id=user.get('id')
    )

    db.add(todo_model)
    db.commit()

    return RedirectResponse(url='/todo_pages', status_code=status.HTTP_302_FOUND)


@router.get('/edit-todo/{todo_id}', response_class=HTMLResponse)
async def edit_todo(
        request: Request,
        todo_id: int,
        db: Session = Depends(get_db)
):
    user = await get_current_user_http(request=request, db=db)
    if user is None:
        return RedirectResponse('/auth', status_code=status.HTTP_302_FOUND)

    todo = db.query(Todos).filter(Todos.id == todo_id).first()
    return templates.TemplateResponse('edit-todo.html', context={'request': request, 'todo': todo})


@router.post('/edit-todo/{todo_id}', response_class=HTMLResponse)
async def edit_todo_commit(
        request: Request,
        todo_id: int,
        title: str = Form(...),
        description: str = Form(...),
        priority: int = Form(...),
        db: Session = Depends(get_db)
) -> RedirectResponse:
    user = await get_current_user_http(request=request, db=db)
    if user is None:
        return RedirectResponse('/auth', status_code=status.HTTP_302_FOUND)

    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    todo_model.title = title
    todo_model.description = description
    todo_model.priority = priority
    db.add(todo_model)
    db.commit()

    return RedirectResponse(url='/todo_pages', status_code=status.HTTP_302_FOUND)


@router.get('/delete/{todo_id}', response_class=HTMLResponse)
async def delete_todo(request: Request, todo_id: int, db: Session = Depends(get_db)) -> RedirectResponse:
    user = await get_current_user_http(request=request, db=db)
    if user is None:
        return RedirectResponse('/auth', status_code=status.HTTP_302_FOUND)

    todo_model = db.query(Todos).filter(
        Todos.id == todo_id,
        Todos.user_id == user.get('id')
    ).first()

    if todo_model is None:
        return RedirectResponse(url='/todo_pages', status_code=status.HTTP_302_FOUND)

    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()
    return RedirectResponse(url='/todo_pages', status_code=status.HTTP_302_FOUND)


@router.get('/complete/{todo_id}', response_class=HTMLResponse)
async def complete_todo(request: Request, todo_id: int, db: Session = Depends(get_db)) -> RedirectResponse:
    user = await get_current_user_http(request=request, db=db)
    if user is None:
        return RedirectResponse('/auth', status_code=status.HTTP_302_FOUND)

    todo = db.query(Todos).filter(Todos.id == todo_id).first()
    todo.complete = not todo.complete
    db.add(todo)
    db.commit()
    return RedirectResponse(url='/todo_pages', status_code=status.HTTP_302_FOUND)
