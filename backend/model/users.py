from database.connection import custom_base
from model.base_mixin import BaseMixin
from sqlalchemy import Column, Enum, String

class Users(custom_base, BaseMixin):
    __tablename__ = "users"
    username = Column(String(length=255), nullable=False, unique=True)
    nickname = Column(String(length=255), nullable=False, unique=True)
    password = Column(String(length=2000), nullable=False)              
    status = Column(Enum("ACTIVE", "DELETED", "BLOCKED"), default="ACTIVE")
    role = Column(Enum("USER", "MANAGER", "ADMIN"), default="USER")  