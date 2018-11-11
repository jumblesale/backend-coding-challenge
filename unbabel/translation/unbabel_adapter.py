from typing import Optional, Mapping, List

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

    def get_all_translations(self) -> Optional[Translation]:
        return get_all_translations(
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


def _create_translation_from_response_json(response_json: dict) -> Translation:
    return create_translation(
        uid=response_json['uid'],
        status=response_json['status'],
        text=response_json.get('text', None),
        translated_text=response_json.get('translated_text', None),
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

    if response.status_code == 200:
        raise TranslationFailedException(response.text)

    json_data = response.json()

    return _create_translation_from_response_json(json_data)


def get_all_translations(
        user_name: str,
        api_key:   str,
        base_url:  str,
) -> List[Translation]:
    response = requests.get(
        url=f'{base_url}/translation/',
        headers=_create_headers(user_name=user_name, api_key=api_key),
    )

    response_json = response.json()

    return list(map(
        _create_translation_from_response_json,
        response_json['objects']
    ))
