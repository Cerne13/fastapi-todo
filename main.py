from fastapi import FastAPI, Depends
from database import engine

from routes import auth, todos, users, address

app = FastAPI(title='Todo App')

# models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(users.router)
app.include_router(address.router)
