from safekeeper import app_config
from safekeeper.repositories import rbac_repo
from safekeeper.services.rbac import RBACService


rbac_service = RBACService(rbac_repo=rbac_repo, config=app_config)
