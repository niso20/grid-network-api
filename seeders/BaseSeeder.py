from seeders.Roles import seedRoles
from seeders.Users import seedUsers

async def runSeeders():
    await seedRoles()
    await seedUsers()