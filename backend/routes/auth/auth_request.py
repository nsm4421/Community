from pydantic.main import BaseModel

class RegisterRequest(BaseModel):
    username:str = None
    password:str = None
    nickname:str = None