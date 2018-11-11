from typing import Optional, List

import attr

from unbabel.types import Uid, SupportsPerformingTranslations, Translation, StatusOption


@attr.s(frozen=True, auto_attribs=True)
class TestTranslationAdapter(SupportsPerformingTranslations):
    def translate(self, text: str) -> Uid:
        return Uid('xyz543')

    def get_translation(self, uid: Uid) -> Optional[Translation]:
        return {
            Uid('abc321'): Translation(
                uid=Uid('abc321'),
                status=StatusOption.completed,
                text='text',
                translated_text='short text'
            ),
            Uid('xyz543'): Translation(
                uid=Uid('xyz543'),
                status=StatusOption.completed,
                text='text',
                translated_text='a very long piece of text'
            ),
        }.get(uid, None)

    def get_all_translations(self) -> List[Translation]:
        return [
            Translation(
                uid=Uid('abc321'),
                status=StatusOption.completed,
                text=None,
                translated_text=None,
            ),
            Translation(
                uid=Uid('xyz543'),
                status=StatusOption.completed,
                text=None,
                translated_text=None,
            )
        ]
