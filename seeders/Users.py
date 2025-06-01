from database import SessionLocal
from services.UserService import UserService
from services.RoleService import RoleService
from middlewares.DbMiddleware import DB

async def seedUsers():
    db = SessionLocal()

    try:
        userService = UserService(db)
        roleService = RoleService(db)

        users = [
            {
                "firstname": "Akachukwu",
                "surname": "Aneke",
                "username": "akalo",
                "password": "akalo123",
                "roleId": roleService.superAdmin().id
            },
            {
                "firstname": "Admin",
                "surname": "Niso",
                "username": "admin",
                "password": "admin123",
                "roleId": roleService.admin().id
            },
            {
                "firstname": "Manager",
                "surname": "Niso",
                "username": "manager",
                "password": "manager123",
                "roleId": roleService.manager().id
            },
            {
                "firstname": "Operator",
                "surname": "Niso",
                "username": "operator",
                "password": "operator123",
                "roleId": roleService.operator().id
            }
        ]

        for user in users:
            userObj = userService.getUserByUsername(user['username'])

            if not userObj:
                userService.save(user)
    finally:
        # Always close the session
        db.close()