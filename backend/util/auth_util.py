from routes.auth.auth_request import RegisterRequest

import re
import jwt
from datetime import datetime, timedelta
import bcrypt

def validate_register_request(req:RegisterRequest):
    """
        회원가입 정보 규칙
        1. username : 5~20자
        2. nickname : 3~20자
        2. passoword : 영어와 숫자를 조합해서 8~20자로 작명
    """

    # validate username
    username = req.username
    if (len(username)<5 or len(username)>20):
        return dict(success=False, message='유저명은 5~20자로 작명해주세요')
    
    # validate nickname
    nickname = req.nickname
    if (len(nickname)<3 or len(nickname)>20):
        return dict(success=False, message='닉네임은 3~20자로 작명해주세요')

    # validate password
    password = req.password
    if (len(password)<5 or len(password)>20):
        pattern = '^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,20}$'
        if not re.fullmatch(pattern, password):
            return dict(success=False, message='닉네임은 3~20자로 작명해주세요')

    return dict(success=True)


def generate_token(data, secret:str, duration:int=168, algorithm:str="HS256"):
    """
        토큰 생성
        - secret : JWT 비밀키
        - duration : 토큰 유효기간(단위:시간)
        - algorithm : 해싱 알고리즘
    """
    _data = data.copy()
    _data.update({"exp": datetime.utcnow() + timedelta(hours=duration)})
    return jwt.encode(_data, secret, algorithm=algorithm)

def encrypt_password(password:str):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())