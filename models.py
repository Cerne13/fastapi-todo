from sqlalchemy import Column, Boolean, Integer, String, ForeignKey
from sqlalchemy.orm import Relationship, declarative_base
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(5), unique=True, index=True)
    username = Column(String(3), unique=True, index=True)
    first_name = Column(String(3))
    last_name = Column(String(3))
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    todos = Relationship("Todos", back_populates="owner")


class Todos(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(Integer)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    owner = Relationship("Users", back_populates="todos")
