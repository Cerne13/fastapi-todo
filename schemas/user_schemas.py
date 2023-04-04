from pydantic import BaseModel


class CreateUser(BaseModel):
    username: str
    email: str | None = None
    first_name: str
    last_name: str
    password: str
    phone_number: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str | None = None
    first_name: str
    last_name: str
    phone_number: str | None = None


class UserVerification(BaseModel):
    username: str
    password: str
    new_password: str
