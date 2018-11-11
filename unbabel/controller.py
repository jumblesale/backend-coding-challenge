import attr

from unbabel.types import SupportsPerformingTranslations


@attr.s(frozen=True, auto_attribs=True)
class Controller:
    translation_adapter: SupportsPerformingTranslations

    def get_translations(self):
        ...
