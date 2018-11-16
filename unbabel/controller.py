from typing import List

import attr

from unbabel.types import SupportsPerformingTranslations, Translation, SupportsStoringUids


@attr.s(frozen=True, auto_attribs=True)
class Controller:
    translation_adapter: SupportsPerformingTranslations
    storage_adapter:     SupportsStoringUids

    def get_translations(self) -> List[Translation]:
        return get_translations(translation_adapter=self.translation_adapter)

    def submit_translation(self, text: str) -> None:
        return submit_translation(text=text, translation_adapter=self.translation_adapter)


def get_translations(
        translation_adapter: SupportsPerformingTranslations
) -> List[Translation]:
    all_translations = translation_adapter.get_all_translations()
    full_translations = [translation for translation in list(map(
        lambda t: translation_adapter.get_translation(t.uid),
        all_translations,
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
        translation_adapter: SupportsPerformingTranslations
) -> None:
    translation_adapter.translate(text=text)
