from fastapi import FastAPI, HTTPException
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette import status
from starlette.responses import RedirectResponse

from routes import auth, todos, users, address, todo_pages

app = FastAPI(title='Todo App')
app.mount('/static', StaticFiles(directory='static'), name='static')


@app.get('/')
async def root():
    return RedirectResponse('/todo_pages', status_code=status.HTTP_302_FOUND)


app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(users.router)
app.include_router(address.router)
app.include_router(todo_pages.router)


# @app.exception_handler(404)
# async def not_found_exception_handler(request: Request, exc: HTTPException):
#     return RedirectResponse('https://fastapi.tiangolo.com')
