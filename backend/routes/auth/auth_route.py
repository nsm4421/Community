from routes.auth.auth_request import RegisterRequest, LoginRequest
from routes.auth.auth_response import User, Token
from model.users import Users
from database.connection import custom_database
from config.const import JWT_SECRET, JWT_ALGORITHM, API_PREFIX
from util.auth_util import validate_register_request, generate_token, encrypt_password

import bcrypt
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

auth_router = APIRouter(prefix="/auth")

@auth_router.post(API_PREFIX+"/register", status_code=201, response_model=Token)
async def register(req:RegisterRequest, session:Session = Depends(custom_database.session)):

    # validate fields
    validation = validate_register_request(req)
    if not validation.get('success'):
        return JSONResponse(status_code=400, content=dict(message=validation.get('message', 'ERROR')))

    # check duplicated or not
    if Users.get_first(session, username=req.username):
        return JSONResponse(status_code=400, content=dict(message='Duplicated username'))
    if Users.get_first(session, username=req.nickname):
        return JSONResponse(status_code=400, content=dict(message='Duplicated nickname'))
    
    # add user
    user = Users.create(session=session, username=req.username, nickname=req.nickname, password=encrypt_password(req.password), auto_commit=True)

    # return token
    data = User.from_orm(user).dict(exclude={'password'})
    token = f'Bearer {generate_token(data=data, secret=JWT_SECRET, algorithm=JWT_ALGORITHM)}'
    return dict(Authorization=token)

@auth_router.post(API_PREFIX+"/login", status_code=201, response_model=Token)
async def login(req:LoginRequest, session:Session = Depends(custom_database.session)):

    user = Users.get_first(session=session, username=req.username)

    if not user:
        return JSONResponse(status_code=400, content=dict(message='Username not exists...'))

    if Users.check_password(raw_password=req.password):
        return JSONResponse(status_code=400, content=dict(message='Invalid password...'))
    
    data = User.from_orm(user).dict(exclude={'password'})
    token = f'Bearer {generate_token(data=data, secret=JWT_SECRET, algorithm=JWT_ALGORITHM)}'
    return dict(Authorization=token)