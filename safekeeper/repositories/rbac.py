from typing import Optional

from sqlalchemy import func

from safekeeper.infras.db.connection import DBConnectionHandler
from safekeeper.interfaces.repositories.rabc_repository import IRBACRepository
from safekeeper.models import (
    Scope,
    PermissionScope,
    Permission,
    RolePermission,
    UserRole,
)


class RBACRepository(IRBACRepository):
    def __init__(self, db: DBConnectionHandler):
        self.session = db.session

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
