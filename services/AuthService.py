from middlewares.DbMiddleware import DB
from typing import TypedDict, Optional
from datetime import timedelta,datetime, timezone
from jose import jwt
import os
from models import User
from passlib.context import CryptContext
from services.UserService import UserService

class UserLogin(TypedDict):
    username: Optional[str] = None
    password: Optional[str] = None

class AuthService:

    def __init__(self, db:DB):
        self.__db = db

    def authenticate(self, data:UserLogin):
        bcryptContext = CryptContext(schemes=['bcrypt'], deprecated='auto')
        userService = UserService(self.__db)

        user = userService.getUserByUsername(data["username"])
        if not user:
            return False

        if not bcryptContext.verify(data["password"], user.password):
            return False

        return user

    def getAccessToken(self, user:User, ):
        secretKey = os.getenv("JWT_SECRET")
        Algorithm = 'HS256'
        encode = {
            'id': user.id,
            'username': user.username,
            'firstname': user.firstname,
            'surname': user.surname,
            'role': {
                'id': user.role.id,
                'name': user.role.name
            } if user.role else None
        }
        minsToExpire = 60*60*60
        expires = datetime.now(timezone.utc) + timedelta(minsToExpire)
        encode.update({'exp': expires})

        return {'token': jwt.encode(encode, secretKey, algorithm=Algorithm), 'expiry': minsToExpire}
