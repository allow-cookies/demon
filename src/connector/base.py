from abc import ABC, abstractmethod
from typing import Generator

from project.dto import ProjectDTO


class PlatformConnector(ABC):
    @abstractmethod
    def list_projects(self) -> Generator[ProjectDTO, None, None]:
        pass
