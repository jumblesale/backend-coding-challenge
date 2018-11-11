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


def _request_translation(
        text:      str,
        user_name: str,
        api_key:   str,
        base_url:  str,
):
    return requests.post(
        url=f'{base_url}/translation',
        headers={
            'Authorization': f'ApiKey {user_name}:{api_key}',
            'Content-Type':  'application/json',
        },
        data={
            'source_language': 'en',
            'target_language': 'es',
            'text_format':     'text',
            'text':            text,
        }
    )


def translate(
        text:      str,
        user_name: str,
        api_key:   str,
        base_url:  str,
) -> Uid:
    response = _request_translation(
        text=text,
        user_name=user_name,
        api_key=api_key,
        base_url=base_url,
    )

    json_response = response.json()

    print(json_response)

    return Uid(json_response['uid'])
