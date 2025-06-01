from services.RoleService import RoleService
from middlewares.DbMiddleware import DB

async def seedRoles(db: DB):
    roleService = RoleService(db)

    roles = ["super admin", "admin", "manager", "operator"]

    for role in roles:
        roleObj = roleService.getRoleByName(role)

        if not roleObj:
            data = { "name": role }
            roleService.save(data)