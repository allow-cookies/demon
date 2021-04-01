from __future__ import annotations

from typing import Iterable, Type

from dependency.parser.base import BaseParser
from dependency.parser.javascript import PackageLockJsonParser, YarnLockParser
from dependency.parser.python import PipfileLockParser, RequirementsTxtParser
from project.models import ProjectDependency


class ParserProvider:
    def __init__(self):
        self._parsers: dict[str, Type[BaseParser]] = {}

    def register(self, file_type: str, parser: Type[BaseParser]) -> ParserProvider:
        self._parsers[file_type] = parser
        return self

    def provide(self, file_type: str) -> Type[BaseParser]:
        return self._parsers[file_type]

    def list_registered_file_types(self) -> Iterable[str]:
        return self._parsers.keys()

    def all(self) -> dict[str, Type[BaseParser]]:
        return self._parsers


source_file_choices = ProjectDependency.SourceTypeChoices

parser_provider = (
    ParserProvider()
    .register(str(source_file_choices.REQUIREMENTS_TXT), RequirementsTxtParser)
    .register(str(source_file_choices.PIPFILE_LOCK), PipfileLockParser)
    .register(str(source_file_choices.PACKAGE_LOCK_JSON), PackageLockJsonParser)
    .register(str(source_file_choices.YARN_LOCK), YarnLockParser)
)
