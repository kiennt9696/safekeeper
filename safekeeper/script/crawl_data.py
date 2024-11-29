import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from safekeeper.models import (
    Role,
    Scope,
    PermissionScope,
    Permission,
    RolePermission,
    UserRole,
    User,
    PermissionAction,
    PermissionObject,
)

if __name__ == "__main__":
    db_uri = "postgresql+psycopg2://postgres:postgres@127.0.0.1:8432/access?application_name=safekeeper"
    engine = create_engine(db_uri)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Fetch data from tables
    data = {
        "roles": [r.__dict__ for r in session.query(Role).all()],
        "permissions": [p.__dict__ for p in session.query(Permission).all()],
        "permission_actions": [
            p.__dict__ for p in session.query(PermissionAction).all()
        ],
        "permission_objects": [
            p.__dict__ for p in session.query(PermissionObject).all()
        ],
        "scopes": [s.__dict__ for s in session.query(Scope).all()],
        "role_permissions": [rp.__dict__ for rp in session.query(RolePermission).all()],
        "permission_scopes": [
            ps.__dict__ for ps in session.query(PermissionScope).all()
        ],
        "users": [ps.__dict__ for ps in session.query(User).all()],
        "user_roles": [ps.__dict__ for ps in session.query(UserRole).all()],
    }

    # Remove SQLAlchemy metadata fields like _sa_instance_state
    for table in data.values():
        for row in table:
            row.pop("_sa_instance_state", None)
            row.pop("updated_at", None)
            row.pop("created_at", None)

    # Save to JSON file
    with open("rbac_base_data.json", "w") as f:
        json.dump(data, f, indent=4)

    print("Base data exported to rbac_base_data.json")
