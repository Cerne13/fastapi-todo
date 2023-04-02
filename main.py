from fastapi import FastAPI, Depends
from database import engine

from routes import auth, todos, users, address
from company import company_apis, dependencies

app = FastAPI(title='Todo App')

# models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(users.router)
app.include_router(address.router)

app.include_router(
    company_apis.router,
    prefix='/company',
    tags=['company'],
    dependencies=[Depends(dependencies.get_token_header)],
    responses={
        404: {'description': 'Not found'},
        418: {'description': 'Internal use only'}
    }
)
