from fastapi import  APIRouter, Depends, HTTPException, Path
from starlette import status
from typing import List
from typing_extensions import TypedDict
from middlewares.DbMiddleware import DB
from resources.UserResource import UserResource
from requests.LoginRequest import Login

from services.AuthService import AuthService

router = APIRouter(prefix='/auth', tags=['auth'])

class AuthResponse(TypedDict):
    user: UserResource
    token: str
    expiry: int

@router.post('/login', status_code=status.HTTP_200_OK, response_model=AuthResponse)
async def login(db: DB, request: Login):
    authService = AuthService(db)

    data = request.model_dump()

    user = authService.authenticate(data)

    if not user:
        raise HTTPException(status_code=400, detail="username or password is incorrect")

    accessToken = authService.getAccessToken(user)

    return {
        'user': user,
        'token': accessToken['token'],
        'expiry': accessToken['expiry']
    }




