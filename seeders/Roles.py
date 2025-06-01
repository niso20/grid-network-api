from database import SessionLocal
from services.RoleService import RoleService
from middlewares.DbMiddleware import DB
from enums.Role import Role as RoleEnum

async def seedRoles():
    db = SessionLocal()
    try:
        # Create the service with the session
        roleService = RoleService(db)

        # Your seeding logic
        roles = [RoleEnum.SUPER_ADMIN, RoleEnum.ADMIN, RoleEnum.MANAGER, RoleEnum.OPERATOR]

        for role in roles:
            # Check if role already exists
            roleObj = roleService.getRoleByName(role)
            if not roleObj:
                # Create the role if it doesn't exist
                roleService.save({"name": role})
                print(f"Created role: {role}")

    finally:
        # Always close the session
        db.close()