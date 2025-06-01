from middlewares.DbMiddleware import DB
from typing import TypedDict, Optional
from models import User
from passlib.context import CryptContext

class UserType(TypedDict):
    firstname: Optional[str] = None
    surname: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    roleId: Optional[str] = None

class UserService:

    def __init__(self, db:DB):
        self.__db = db

    def save(self, data:UserType):
        bcryptContext = CryptContext(schemes=['bcrypt'], deprecated='auto')

        userModel = User(
            firstname=data["firstname"],
            surname=data.get("surname"),
            username=data["username"],
            password=bcryptContext.hash(data["password"]),
            role_id=data["roleId"]
        )

        self.__db.add(userModel)
        self.__db.commit()
        self.__db.refresh(userModel)

        return userModel

    def update(self, data:UserType, user:User):
        if "firstname" in data and data["firstname"] is not None: user.firstname = data["firstname"]
        if "surname" in data and data["surname"] is not None: user.surname = data["surname"]
        if "username" in data and data["username"] is not None: user.username = data["username"]
        if "roleId" in data and data["roleId"] is not None: user.role_id = data["roleId"]

        self.__db.commit()
        self.__db.refresh(user)

        return user

    def getUsers(self):
        return self.__db.query(User).all()

    def getUser(self, id):
        return self.__db.query(User).filter(User.id == id).first()
    
    def getUserByUsername(self, username):
        return self.__db.query(User).filter(User.username == username).first()
