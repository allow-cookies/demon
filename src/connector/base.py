from abc import ABC, abstractmethod
from typing import Generator
from uuid import UUID

from dependency.dto import DependencyDTO
from project.dto import ProjectDTO


class PlatformConnector(ABC):
    @abstractmethod
    def __init__(self, user_id: UUID):
        pass

    @abstractmethod
    def list_projects(self) -> Generator[ProjectDTO, None, None]:
        pass

    @abstractmethod
    def list_dependencies(self, project_id) -> Generator[DependencyDTO, None, None]:
        pass
