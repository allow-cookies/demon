from __future__ import annotations

from typing import Iterable, Type

from dependency.parser.base import BaseParser
from dependency.parser.python import RequirementsTxtParser


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


parser_provider = ParserProvider().register("requirements.txt", RequirementsTxtParser)
