from typing import Optional

from pydantic import BaseModel


class CreateUser(BaseModel):
    username: str
    email: Optional[str]
    first_name: str
    last_name: str
    password: str
    phone_number: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: Optional[str]
    first_name: str
    last_name: str
    phone_number: Optional[str]


class UserVerification(BaseModel):
    username: str
    password: str
    new_password: str