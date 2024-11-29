from safekeeper.extension import db
from safekeeper.repositories.rbac import RBACRepository


rbac_repo = RBACRepository(db=db)
