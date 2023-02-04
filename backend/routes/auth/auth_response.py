from pydantic.main import BaseModel

class User(BaseModel):
    id: int
    username: str = None
    nickname: str = None
    password: str = None
    class Config:
        orm_mode = True

class Token(BaseModel):
    Authorization: str = None   
    class Config:
        orm_mode = True