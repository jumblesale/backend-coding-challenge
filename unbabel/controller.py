import attr

from unbabel.types import SupportsPerformingTranslations


@attr.s(frozen=True, auto_attribs=True)
class Controller:
    translation_adapter: SupportsPerformingTranslations

    def get_translations(self):
        all_translations = self.translation_adapter.get_all_translations()
        full_translations = list(map(
            lambda t: self.translation_adapter.get_translation(t.uid),
            all_translations
        ))
