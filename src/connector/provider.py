from __future__ import annotations
from typing import Type
from uuid import UUID

from connector.base import PlatformConnector
from connector.gitlab import GitLabConnector
from user_platform.models import UserPlatform


class ConnectorProvider:
    def __init__(self):
        self._connectors: dict[str, Type[PlatformConnector]] = {}

    def register(self, platform_name: str, platform_connector: Type[PlatformConnector]) -> ConnectorProvider:
        self._connectors[platform_name] = platform_connector
        return self

    def provide(self, platform_name: str, user_id: UUID) -> PlatformConnector:
        connector_class = self._connectors[platform_name]
        return connector_class(user_id=user_id)


connector_provider = (
    ConnectorProvider()
    .register(
        platform_name=UserPlatform.PlatformChoices.GITLAB.name,
        platform_connector=GitLabConnector,
    )
)
