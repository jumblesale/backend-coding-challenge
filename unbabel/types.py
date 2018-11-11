from typing import NewType

from typing_extensions import Protocol

Uid = NewType('Uid', str)


class TranslationFailedException(Exception):
    ...


class SupportsPerformingTranslations(Protocol):
    def translate(self, text: str) -> Uid:
        ...
