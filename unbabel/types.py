from enum import Enum
from typing import NewType, NamedTuple, Optional, List

from typing_extensions import Protocol

Uid = NewType('Uid', str)


class TranslationFailedException(Exception):
    ...


class StatusOption(Enum):
    translating = 'translating'
    completed = 'completed'
    new = 'new'
    unknown = 'unknown'


def string_to_status_option(status: str) -> StatusOption:
    return {
        'translating': StatusOption.translating,
        'completed':   StatusOption.completed,
        'new':         StatusOption.new,
    }.get(status, StatusOption.unknown)


Translation = NamedTuple('Translation', [
    ('uid',             Uid),
    ('status',          StatusOption),
    ('text',            Optional[str]),
    ('translated_text', Optional[str]),
])


def create_translation(
        uid:             str,
        status:          str,
        text:            Optional[str] = None,
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

    def get_all_translations(self) -> List[Translation]:
        ...


class SupportsStoringUids(Protocol):
    def store_uid(self, uid: Uid) -> None:
        ...

    def retrieve_all_uids(self) -> List[Uid]:
        ...
