from abc import ABC, abstractmethod
from typing import Generator

from dependency.dto import DependencyDTO


class BaseParser(ABC):
    @classmethod
    @abstractmethod
    def parse(
        cls, from_file: str, contents: str
    ) -> Generator[DependencyDTO, None, None]:
        pass
