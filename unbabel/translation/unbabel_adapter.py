import attr
import requests

from unbabel.types import SupportsPerformingTranslations, Uid


@attr.s(frozen=True, auto_attribs=True)
class UnbabelAdapter(SupportsPerformingTranslations):
    user_name: str
    api_key:   str
    base_url:  str

    def translate(self, text: str) -> Uid:
        return translate(
            text=text,
            user_name=self.user_name,
            api_key=self.api_key,
            base_url=self.base_url,
        )


def translate(
        text:      str,
        user_name: str,
        api_key:   str,
        base_url:  str,
) -> Uid:
    ...
