from operator import truediv

from fastapi import Depends, HTTPException
from starlette import status
import os
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from database import engine, SessionLocal
from typing import Annotated
from sqlalchemy.orm import  Session
from services.UserService import UserService
from services.RoleService import RoleService
from enums.Role import Role

SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = 'HS256'
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/login')

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        print(token)
        db = SessionLocal()
        userService = UserService(db)
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        userId: int = payload.get('id')

        if userId is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')

        user = userService.getUser(userId)

        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')

        return user
    except JWTError:
        print('an error occurred')
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')
    finally:
        db.close()

def require_role(required_role: str):
    async def role_checker(user=Depends(get_current_user)):
        if validRole(user, required_role):
            return user
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='You are not authorized to perform this operation'
            )
    return role_checker

def validRole(user, role):
    valid = []
    match role:
        case Role.SUPER_ADMIN:
            if user.role.name == Role.SUPER_ADMIN:
                valid = [Role.SUPER_ADMIN]
        case Role.ADMIN:
            valid = [Role.SUPER_ADMIN, Role.ADMIN]
        case Role.MANAGER:
            valid = [Role.SUPER_ADMIN, Role.ADMIN, Role.MANAGER]
        case Role.OPERATOR:
            valid = [Role.SUPER_ADMIN, Role.ADMIN, Role.MANAGER, Role.OPERATOR]

    if user.role.name in valid:
        return True
    else:
        return False

# Convenience dependency annotations
User = Annotated[dict, Depends(get_current_user)]
SuperAdminUser = Annotated[dict, Depends(require_role(Role.SUPER_ADMIN))]
AdminUser = Annotated[dict, Depends(require_role(Role.ADMIN))]
ManagerUser = Annotated[dict, Depends(require_role(Role.MANAGER))]
OperatorUser = Annotated[dict, Depends(require_role(Role.OPERATOR))]