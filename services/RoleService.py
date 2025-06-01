from middlewares.DbMiddleware import DB
from typing import TypedDict, Optional
from sqlalchemy import select
from models import Role
from enums.Role import Role as RoleEnum

class RoleType(TypedDict):
    name: Optional[str] = None

class RoleService:

    def __init__(self, db:DB):
        self.__db = db
        self.__role = select(Role)

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
        # return self.__db.execute(self.__role).scalars().all()
        return self.__db.query(Role).all()

    def getRole(self, id):
        # stmt = select(Role).where(Role.id == id)
        # return self.__db.execute(stmt).scalar_one_or_none()
        return self.__db.query(Role).filter(Role.id == id).first()

    def getRoleByName(self, name):
        # stmt = select(Role).where(Role.name == name)
        # return self.__db.execute(stmt).scalar_one_or_none()
        return self.__db.query(Role).filter(Role.name == name).first()

    def superAdmin(self):
        return self.getRoleByName(RoleEnum.SUPER_ADMIN)

    def admin(self):
        return self.getRoleByName(RoleEnum.ADMIN)

    def manager(self):
        return self.getRoleByName(RoleEnum.MANAGER)

    def operator(self):
        return self.getRoleByName(RoleEnum.OPERATOR)
