from enum import Enum

class Role(str, Enum):
    SUPER_ADMIN = "super admin"
    ADMIN = "admin"
    MANAGER = "manager"
    OPERATOR = "operator"