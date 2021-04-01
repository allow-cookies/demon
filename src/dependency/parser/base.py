from abc import ABC, abstractmethod
from re import Pattern
from typing import Generator

from dependency.dto import DependencyDTO


class BaseParser(ABC):
    @classmethod
    @abstractmethod
    def parse(
        cls, source_file: str, contents: bytes
    ) -> Generator[DependencyDTO, None, None]:
        pass

    @classmethod
    @abstractmethod
    def source_file_regex(cls) -> Pattern:
        pass
