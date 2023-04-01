from typing import Optional

from pydantic import BaseModel


class CreateUser(BaseModel):
    username: str
    email: Optional[str]
    first_name: str
    last_name: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: Optional[str]
    first_name: str
    last_name: str


class UserVerification(BaseModel):
    username: str
    password: str
    new_password: str