from enum import Enum


class PermissionEnum(str, Enum):
    # Acciones y permisos relacionados con los usuarios
    READ_USER = ("Read user", "read", "RUSO")
    UPDATE_USER = ("Update user", "update", "UUSO")
    DEACTIVATE_USER = ("Delete user", "deactivate", "DUSO")


    def __new__(cls, value, action, code):
        obj = str.__new__(cls)
        obj._value_ = value
        obj.action = action
        obj.code = code
        return obj
