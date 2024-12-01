from abc import ABC, abstractmethod
from typing import Optional


class IRBACRepository(ABC):

    @abstractmethod
    def has_scopes(self, user_id: str, scopes: list[str]) -> Optional[bool]:
        pass

    @abstractmethod
    def get_permissions(self, user_id: str) -> (str, list):
        pass
