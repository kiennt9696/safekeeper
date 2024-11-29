from abc import ABC, abstractmethod
from typing import Optional


class IRBACRepository(ABC):

    @abstractmethod
    def has_scopes(self, user_id: str, scopes: list[str]) -> Optional[bool]:
        pass
