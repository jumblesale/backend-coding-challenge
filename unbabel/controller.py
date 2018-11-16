from typing import List

import attr

from unbabel.types import SupportsPerformingTranslations, Translation, SupportsStoringUids, Uid


@attr.s(frozen=True, auto_attribs=True)
class Controller:
    translation_adapter: SupportsPerformingTranslations
    storage_adapter:     SupportsStoringUids

    def get_translations(self) -> List[Translation]:
        return get_translations(
            uids=self.storage_adapter.retrieve_all_uids(),
            translation_adapter=self.translation_adapter
        )

    def submit_translation(self, text: str) -> None:
        return submit_translation(
            text=text,
            translation_adapter=self.translation_adapter,
            storage_adapter=self.storage_adapter,
        )


def get_translations(
        uids:                List[Uid],
        translation_adapter: SupportsPerformingTranslations
) -> List[Translation]:
    full_translations = [translation for translation in list(map(
        translation_adapter.get_translation,
        uids,
    )) if translation is not None]

    # filter out None values before comparing
    sorted_translations = sorted(
        [t for t in full_translations if t.translated_text is not None],
        key=lambda t: (len(t.translated_text), t),  # type: ignore
        reverse=True
    )

    # join the Nones back into the list at the end
    return [
        *sorted_translations,
        *[t for t in full_translations if t.translated_text is None]
    ]


def submit_translation(
        text:                str,
        translation_adapter: SupportsPerformingTranslations,
        storage_adapter:     SupportsStoringUids
) -> None:
    uid = translation_adapter.translate(text=text)
    storage_adapter.store_uid(uid)
