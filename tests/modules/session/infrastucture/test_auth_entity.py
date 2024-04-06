from datetime import datetime, timezone
from app.modules.auth.domain.entities import Permission, PermissionRole, Role
from sqlalchemy.orm import Session

def test_permission_role_relationships():
    
    permission = Permission(action="read", code="READ", name="Read", created_at=datetime.now(timezone.utc))
    role = Role(code="ADMIN", name="Admin", created_at=datetime.now(timezone.utc))
    
    permission_role = PermissionRole(permission=permission, role=role)

    assert permission_role.permission == permission
    assert permission_role.role == role

def test_permission_str_representation():
    permission = Permission(action="read", code="READ", name="Read", created_at=datetime.now(timezone.utc))
    assert str(permission) == "Read"

def test_role_str_representation():
    role = Role(code="ADMIN", name="Admin", created_at=datetime.now(timezone.utc))
    assert str(role) == "Admin"