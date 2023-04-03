from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from routes import auth, todos, users, address

app = FastAPI(title='Todo App')
app.mount('/static', StaticFiles(directory='static'), name='static')

# models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(users.router)
app.include_router(address.router)
