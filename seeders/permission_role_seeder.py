from sqlalchemy import and_
from sqlalchemy.orm import Session
from app.modules.auth.domain.entities import PermissionRole, Role, Permission
from app.modules.auth.domain.enums.permission_enum import PermissionEnum
from app.modules.auth.domain.enums.role_enum import RoleEnum


def permission_roles_seed(db: Session) -> None:
    roles_and_permissions = {
        RoleEnum.SUPER_USUARIO.value: [
            PermissionEnum.READ_USER,
            PermissionEnum.UPDATE_USER,
            PermissionEnum.DEACTIVATE_USER
        ],
        RoleEnum.TERCERO.value: [
            PermissionEnum.READ_USER,
            PermissionEnum.UPDATE_USER
        ],
        RoleEnum.DEPORTISTA.value: [
            PermissionEnum.READ_USER,
            PermissionEnum.UPDATE_USER
        ]
    }
    assign_permission_to_roles(db, roles_and_permissions)


def assign_permission_to_roles(db: Session, roles_and_permissions) -> None:
    for role_code, permissions in roles_and_permissions.items():
        role_name = RoleEnum.lookup_by_code(role_code)
        role_db = create_or_update_role(db, Role(code=role_code, name=role_name))

        for permission_info in permissions:
            permission_db = create_or_update_permission(db, permission_info)

            association = PermissionRole(role_id=role_db.id, permission_id=permission_db.id)
            create_or_update_permission_role(db, association)


def create_or_update_role(db: Session, role: Role) -> Role:
    role_db = db.query(Role).filter_by(code=role.code).first()

    if role_db:
        role_db.code = role.code
        role_db.name = role.name
    else:
        role_db = role
        db.add(role_db)

    db.commit()
    return role_db


def create_or_update_permission(db: Session, permission_info: Permission) -> Permission:
    permission_db = db.query(Permission).filter_by(code=permission_info.code).first()

    if permission_db:
        permission_db.action = permission_info.action,
        permission_db.code = permission_info.code,
        permission_db.name = permission_info.value
    else:
        permission_db = Permission(
            action=permission_info.action,
            code=permission_info.code,
            name=permission_info.value
        )
        db.add(permission_db)

    db.commit()
    return permission_db


def create_or_update_permission_role(db: Session, permission_role: PermissionRole) -> None:
    permission_role_db = db.query(PermissionRole) \
        .filter(
        and_(
            PermissionRole.role_id == permission_role.role_id,
            PermissionRole.permission_id == permission_role.permission_id
        )).first()

    if not permission_role_db:
        permission_role_db = PermissionRole(
            role_id=permission_role.role_id,
            permission_id=permission_role.permission_id
        )
        db.add(permission_role_db)

    db.commit()
