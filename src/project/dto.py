from dataclasses import dataclass
from typing import Iterable

from django.utils.datetime_safe import datetime

from dependency.dto import DependencyDTO


@dataclass(frozen=True)
class ProjectDTO:
    external_id: str
    name: str
    description: str
    path: str
    created_at: datetime
    dependencies: Iterable[DependencyDTO]
