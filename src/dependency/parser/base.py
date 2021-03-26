from abc import ABC, abstractmethod
from typing import Generator

from dependency.dto import DependencyDTO


class BaseParser(ABC):
    @classmethod
    @abstractmethod
    def parse(
        cls, source_file: str, contents: bytes
    ) -> Generator[DependencyDTO, None, None]:
        pass
