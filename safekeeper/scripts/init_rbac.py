import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from safekeeper.models import (
    Role,
    Permission,
    Scope,
    RolePermission,
    PermissionScope,
    PermissionAction,
    User,
    UserRole,
    PermissionObject,
)

if __name__ == "__main__":

    db_uri = "postgresql+psycopg2://postgres:postgres@127.0.0.1:8432/access?application_name=safekeeper"
    engine = create_engine(db_uri)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Load data from JSON file
    with open("rbac_base_data.json", "r") as f:
        data = json.load(f)

    # Insert data into tables
    for role in data["roles"]:
        session.add(Role(**role))
        session.flush()

    for scope in data["scopes"]:
        session.add(Scope(**scope))
        session.flush()

    for permission_action in data["permission_actions"]:
        session.add(PermissionAction(**permission_action))
        session.flush()

    for permission_object in data["permission_objects"]:
        session.add(PermissionObject(**permission_object))
        session.flush()

    for permission in data["permissions"]:
        session.add(Permission(**permission))
        session.flush()

    for role_permission in data["role_permissions"]:
        session.add(RolePermission(**role_permission))
        session.flush()

    for permission_scope in data["permission_scopes"]:
        session.add(PermissionScope(**permission_scope))
        session.flush()

    for user in data["users"]:
        session.add(User(**user))
        session.flush()

    for user_role in data["user_roles"]:
        session.add(UserRole(**user_role))
        session.flush()

    # Commit changes
    session.commit()

    print("Base data initialized in the new system")
