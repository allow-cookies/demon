from dataclasses import dataclass


@dataclass(frozen=True)
class DependencyDTO:
    name: str
    version: str
    from_file: str
