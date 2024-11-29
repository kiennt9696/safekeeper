from uuid import uuid4

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean, create_engine
from datetime import datetime

from sqlalchemy.orm import relationship

Base = declarative_base()


def _uuid4():
    return str(uuid4())


class AuditTable(Base):
    __abstract__ = True
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
    updated_by = Column(String, nullable=True)


class User(AuditTable):
    __tablename__ = "user"
    id = Column(String, primary_key=True, default=_uuid4)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=False)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    active = Column(Boolean, default=True)

    roles = relationship("UserRole", back_populates="user")


class Client(AuditTable):
    __tablename__ = "client"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    secret = Column(String, nullable=False)
    redirect_uri = Column(String)
    login_type = Column(String)

    # roles = relationship("ClientRole", back_populates="client")


class Role(AuditTable):
    __tablename__ = "role"
    id = Column(String, primary_key=True, default=_uuid4)
    name = Column(String, nullable=False)
    description = Column(String)
    client_id = Column(String, ForeignKey("client.id"))

    # client = relationship("Client", back_populates="roles")
    users = relationship("UserRole", back_populates="role")
    permissions = relationship("RolePermission", back_populates="role")


class Permission(AuditTable):
    __tablename__ = "permission"
    id = Column(String, primary_key=True, default=_uuid4)
    name = Column(String, nullable=False)
    description = Column(String)
    client_id = Column(String, ForeignKey("client.id"))
    object_id = Column(String, ForeignKey("permission_object.id"))
    action_id = Column(String, ForeignKey("permission_action.id"))

    scopes = relationship("PermissionScope", back_populates="permission")
    roles = relationship("RolePermission", back_populates="permission")


class PermissionObject(AuditTable):
    __tablename__ = "permission_object"
    id = Column(String, primary_key=True, default=_uuid4)
    name = Column(String, nullable=False)


class PermissionAction(AuditTable):
    __tablename__ = "permission_action"
    id = Column(String, primary_key=True, default=_uuid4)
    name = Column(String, nullable=False)


class Scope(AuditTable):
    __tablename__ = "scope"
    id = Column(String, primary_key=True, default=_uuid4)
    name = Column(String, nullable=False)

    permissions = relationship(
        "PermissionScope",
        back_populates="scope",
        cascade="all, delete-orphan",
    )


class PermissionScope(AuditTable):
    __tablename__ = "permission_scope"
    permission_id = Column(String, ForeignKey("permission.id"), primary_key=True)
    scope_id = Column(String, ForeignKey("scope.id"), primary_key=True)

    permission = relationship("Permission", back_populates="scopes")
    scope = relationship("Scope", back_populates="permissions")


class RolePermission(AuditTable):
    __tablename__ = "role_permission"
    role_id = Column(String, ForeignKey("role.id"), primary_key=True)
    permission_id = Column(String, ForeignKey("permission.id"), primary_key=True)

    role = relationship("Role", back_populates="permissions")
    permission = relationship("Permission", back_populates="roles")


class UserRole(Base):
    __tablename__ = "user_role"
    user_id = Column(String, ForeignKey("user.id"), primary_key=True)
    role_id = Column(String, ForeignKey("role.id"), primary_key=True)

    user = relationship("User", back_populates="roles")
    role = relationship("Role", back_populates="users")


class ClientRole(Base):
    __tablename__ = "client_role"
    client_id = Column(String, ForeignKey("client.id"), primary_key=True)
    role_id = Column(String, ForeignKey("role.id"), primary_key=True)

    # client = relationship("Client", back_populates="roles")
    # role = relationship("Role", back_populates="clients")


if __name__ == "__main__":
    db_uri = "postgresql+psycopg2://postgres:postgres@127.0.0.1:8432/access?application_name=safekeeper"
    engine = create_engine(db_uri)
    Base.metadata.create_all(engine)
