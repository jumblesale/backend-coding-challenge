from typing import Optional
from unittest import mock
from unittest.mock import call, MagicMock

import pytest

from unbabel.types import Translation, StatusOption, Uid, SupportsPerformingTranslations
import unbabel.controller as controller


def _create_uid():
    return Uid('xyz543')


def _create_get_translation(
        translated_text: Optional[str],
        status:          Optional[StatusOption] = None,
        uid:             Optional[str] = None,
) -> Translation:
    return Translation(
        uid=Uid(uid) if uid is not None else _create_uid(),
        status=status if status is not None else StatusOption.unknown,
        text='text',
        translated_text=translated_text,
    )


def _create_get_all_translations():
    return [
        _create_get_translation('shorter just 15', uid='1'),
        _create_get_translation('this is the longest string at a huge 39', uid='2'),
        _create_get_translation(None, uid='3'),
        _create_get_translation('this string has length 25', uid='4'),
    ]


@pytest.fixture()
def mock_translation_adapter() -> SupportsPerformingTranslations:
    yield mock.Mock(
        translate=MagicMock(side_effect=_create_uid),
        get_translation=MagicMock(side_effect=_create_get_translation),
        get_all_translations=MagicMock(side_effect=_create_get_all_translations),
    )


def test_it_gets_full_translation_for_each_translation(
        mock_translation_adapter: mock.Mock,
):
    # arrange
    test_controller = controller.Controller(mock_translation_adapter)

    # act
    test_controller.get_translations()

    # assert
    mock_translation_adapter.get_translation.assert_has_calls([
        call(Uid('1')),
        call(Uid('2')),
        call(Uid('3')),
        call(Uid('4')),
    ], any_order=True)
