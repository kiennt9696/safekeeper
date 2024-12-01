from typing import Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from safekeeper.infras.db.connection import DBConnectionHandler
from safekeeper.interfaces.repositories.rabc import IRBACRepository
from safekeeper.models import (
    Scope,
    PermissionScope,
    Permission,
    RolePermission,
    UserRole,
    Role,
)


class RBACRepository(IRBACRepository):
    def __init__(self, db: DBConnectionHandler):
        self.session: Session = db.session

    def has_scopes(self, user_id: str, scopes: list[str]) -> Optional[bool]:

        matching_scopes = (
            self.session.query(func.count(func.distinct(Scope.id)))
            .join(PermissionScope, Scope.id == PermissionScope.scope_id)
            .join(Permission, Permission.id == PermissionScope.permission_id)
            .join(RolePermission, RolePermission.permission_id == Permission.id)
            .join(UserRole, UserRole.role_id == RolePermission.role_id)
            .filter(UserRole.user_id == user_id, Scope.name.in_(scopes))
            .scalar()
        )
        return matching_scopes == len(scopes)

    def get_permissions(self, user_id: str):
        role = (
            self.session.query(Role)
            .join(UserRole, UserRole.role_id == Role.id)
            .filter(UserRole.user_id == user_id)
            .first()
        )

        scopes = (
            self.session.query(Scope.name)
            .select_from(UserRole)
            .join(RolePermission, RolePermission.role_id == UserRole.role_id)
            .join(Permission, Permission.id == RolePermission.permission_id)
            .join(PermissionScope, Permission.id == PermissionScope.permission_id)
            .join(Scope, Scope.id == PermissionScope.scope_id)
            .filter(UserRole.user_id == user_id)
            .filter(UserRole.role_id == role.id)
            .all()
        )
        return role.name, scopes
