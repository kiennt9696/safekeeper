import datetime
from typing import Optional

from common_utils.token import encode_jwt

from safekeeper.interfaces.repositories.rabc import IRBACRepository


class RBACService:
    def __init__(self, config: dict, rbac_repo: IRBACRepository):
        self.config = config
        self.rbac_repo = rbac_repo

    def __generate_access_token(self, scopes: str, current_user: dict):
        token = {
            "type": "access_token",
            "scopes": scopes,
            "sub": current_user.get("sub"),
            "username": current_user.get("username"),
            # 'aud': client,  => for later implementation with client in oauth2 flow
            "exp": datetime.datetime.utcnow()
            + datetime.timedelta(seconds=self.config["TOKEN_EXPIRATION_TIME"]),
        }
        return encode_jwt(token, self.config["PRIVATE_KEY"])

    def __is_user_active(self, username):
        """Assume that user is active"""
        return True

    def __scope_existed(self, scopes: list[str]):
        """Assume that scope is valid"""
        return True

    def __have_privilege(self, current_user: dict, scopes: str) -> bool:
        """
        We need to check various logic flow here but I only want to focus on the permission flow
        """
        scopes = scopes.split(",")
        if not self.__scope_existed(scopes):
            return False
        if not self.__is_user_active(current_user):
            return False
        if not self.rbac_repo.has_scopes(current_user.get("sub"), scopes):
            return False
        return True

    def grant_access(self, current_user: dict, scopes: str) -> Optional[str]:
        """
        This function grants access to a user with the given scopes.
        However, I will only focus on RBAC part only.
        I prefer to implement oauth2 authorization code grant in the future with client id validation. I am going to
        skip that part in this implementation.
        """
        if self.__have_privilege(current_user, scopes):
            return self.__generate_access_token(scopes, current_user)
        return None
