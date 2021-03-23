import re
from typing import Generator

from dependency.dto import DependencyDTO
from dependency.parser.base import BaseParser


class RequirementsTxtParser(BaseParser):
    REGEX = r"([\d\w\-]+)\=\=([\d\w\.]+)"

    @classmethod
    def parse(
        cls, from_file: str, contents: str
    ) -> Generator[DependencyDTO, None, None]:
        return (
            DependencyDTO(
                name=dependency[1],
                version=dependency[2],
                from_file=from_file,
            )
            for dependency in re.finditer(cls.REGEX, contents, re.MULTILINE)
        )
