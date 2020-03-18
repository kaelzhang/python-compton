from abc import ABC, abstractmethod
from typing import (
    List
)

from .vector import Vector


class Consumer(ABC):
    @property
    @abstractmethod
    def vectors(self) -> List[Vector]:
        return

    @abstractmethod
    def should_process(self, *args) -> bool:
        return True

    async def process(self, *args):
        pass
