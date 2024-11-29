from abc import ABC, abstractmethod
from typing import Optional

from safekeeper.models import User


class IUserRepository(ABC):

    @abstractmethod
    def create(self, user_info: dict) -> Optional[User]:
        pass

    @abstractmethod
    def get(self, username: str) -> Optional[User]:
        pass
