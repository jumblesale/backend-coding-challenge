from enum import Enum
from typing import NewType, NamedTuple, Optional

from typing_extensions import Protocol

Uid = NewType('Uid', str)


class TranslationFailedException(Exception):
    ...


class StatusOption(Enum):
    translating = 'translating'
    completed = 'completed'


def string_to_status_option(status: str) -> StatusOption:
    return {
        'translating': StatusOption.translating,
        'completed':   StatusOption.completed,
    }[status]


Translation = NamedTuple('Translation', [
    ('uid',             Uid),
    ('status',          StatusOption),
    ('text',            str),
    ('translated_text', Optional[str]),
])


def create_translation(
        uid:             str,
        status:          str,
        text:            str,
        translated_text: Optional[str] = None,
) -> Translation:
    return Translation(
        uid=Uid(uid), status=string_to_status_option(status),
        text=text, translated_text=translated_text,
    )


class SupportsPerformingTranslations(Protocol):
    def translate(self, text: str) -> Uid:
        ...

    def get_translation(self, uid: Uid) -> Optional[Translation]:
        ...
