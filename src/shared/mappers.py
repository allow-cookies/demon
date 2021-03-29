from shared.constants import SOURCE_FILE_LANGUAGE_MAP


class SourceFileToLanguageMapper:
    @classmethod
    def map(cls, source_file: str) -> str:
        return SOURCE_FILE_LANGUAGE_MAP[source_file]
