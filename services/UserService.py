from middlewares.DbMiddleware import DB
from typing import TypedDict, Optional
from models import Role

class RoleType(TypedDict):
    name: Optional[str] = None

class RoleService:

    def __init__(self, db:DB):
        self.__db = db

    def save(self, data:RoleType):
        roleModel = Role(
            name=data["name"]
        )

        self.__db.add(roleModel)
        self.__db.commit()
        self.__db.refresh(roleModel)

        return roleModel

    def update(self, data:RoleType, role:Role):
        if "name" in data and data["name"] is not None: role.name = data["name"]

        self.__db.commit()
        self.__db.refresh(role)

        return role

    def getRoles(self):
        return self.__db.query(Role).all()

    def getRole(self, id):
        return self.__db.query(Role).filter(Role.id == id).first()
    
    def getRoleByName(self, name):
        return self.__db.query(Role).filter(Role.name == name).first()
