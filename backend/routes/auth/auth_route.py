from routes.auth.auth_request import RegisterRequest
from routes.auth.auth_response import User, Token
from model.users import Users
from database.connection import custom_database
from config.const import JWT_SECRET, JWT_ALGORITHM
from util.auth_util import validate_register_request, generate_token

import bcrypt
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

auth_router = APIRouter(prefix="/auth")

@auth_router.post("/register", status_code=201, response_model=Token)
async def register(req:RegisterRequest, session:Session = Depends(custom_database.session)):
    
    # validate fields
    validation = validate_register_request(req)
    if not validation.get('success'):
        return JSONResponse(status_code=400, content=dict(message=validation.get('message', 'ERROR')))

    # TODO : check whether username, nickname are duplicated or not
    
    # add user
    req.password  = bcrypt.hashpw(req.password.encode('utf-8'), bcrypt.gensalt())
    user = Users.create(session=session, username=req.username, nickname=req.nickname, password=req.password)

    # return token
    data = User.from_orm(user).dict(exclude={'password'})
    token = f'Bearer {generate_token(data=data, secret=JWT_SECRET, algorithm=JWT_ALGORITHM)}'
    return dict(Authorization=token)