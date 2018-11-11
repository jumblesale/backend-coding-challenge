from typing import Optional, Mapping

import attr
import requests

from unbabel.types import SupportsPerformingTranslations, Uid, TranslationFailedException, Translation, \
    create_translation


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

    def get_translation(self, uid: Uid) -> Optional[Translation]:
        return get_translation(
            uid=uid,
            user_name=self.user_name,
            api_key=self.api_key,
            base_url=self.base_url,
        )


def _create_headers(user_name: str, api_key: str) -> Mapping[str, str]:
    return {
        'Authorization': f'ApiKey {user_name}:{api_key}',
        'Content-Type': 'application/json',
    }


def _request_translation(
        text:      str,
        user_name: str,
        api_key:   str,
        base_url:  str,
):
    return requests.post(
        url=f'{base_url}/translation',
        headers=_create_headers(user_name=user_name, api_key=api_key),
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

    if response.status_code // 100 != 2:
        raise TranslationFailedException(response.text)

    json_response = response.json()

    return Uid(json_response['uid'])


def get_translation(
        uid:       Uid,
        user_name: str,
        api_key:   str,
        base_url:  str,
) -> Optional[Translation]:
    response = requests.get(
        url=f'{base_url}/translation/{str(uid)}/',
        headers=_create_headers(user_name=user_name, api_key=api_key),
    )

    if response.status_code == 404:
        return None

    if response.status_code // 100 != 2:
        raise TranslationFailedException(response.text)

    json_data = response.json()

    return create_translation(
        uid=json_data['uid'],
        status=json_data['status'],
        text=json_data['text'],
        translated_text=json_data.get('translated_text', None),
    )
