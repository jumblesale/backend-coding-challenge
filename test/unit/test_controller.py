from typing import Optional, Mapping
from unittest import mock
from unittest.mock import call, MagicMock

import pytest
from hamcrest import equal_to, assert_that

from unbabel.types import Translation, StatusOption, Uid, SupportsPerformingTranslations
import unbabel.controller as controller


translation_uid_map: Mapping[str, Optional[str]] = {
    Uid('1'): 'shorter just 15',
    Uid('2'): 'this is the longest string at a huge 39',
    Uid('3'): None,
    Uid('4'): 'this string has length 25'
}


def _create_get_translation(
        uid: Optional[str] = None,
) -> Translation:
    return Translation(
        uid=Uid(uid),
        status=StatusOption.unknown,
        text='text',
        translated_text=translation_uid_map[uid],
    )


def _create_uid():
    return 'xyz543'


def _create_get_all_translations():
    return [
        _create_get_translation(Uid('1')),
        _create_get_translation(Uid('2')),
        _create_get_translation(Uid('3')),
        _create_get_translation(Uid('4')),
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


def test_it_sorts_translations_by_translation_length_longest_to_shortest(
        mock_translation_adapter: mock.Mock,
):
    # arrange
    test_controller = controller.Controller(mock_translation_adapter)

    # act
    result = test_controller.get_translations()

    # assert
    translated_texts = [(t.uid, t.translated_text) for t in result]
    assert_that(translated_texts, equal_to([
        (Uid('2'), 'this is the longest string at a huge 39'),
        (Uid('4'), 'this string has length 25'),
        (Uid('1'), 'shorter just 15'),
        (Uid('3'), None),
    ]))


def test_it_ignores_translations_which_could_not_be_found(
        mock_translation_adapter: mock.Mock,
):
    # arrange
    mock_translation_adapter.get_translation = MagicMock(side_effect=[
        _create_get_translation('1'),
        None,
    ])
    test_controller = controller.Controller(mock_translation_adapter)

    # act
    result = test_controller.get_translations()

    # assert
    assert_that(len(result), equal_to(1))


def test_it_submits_text_to_get_translated(
        mock_translation_adapter: mock.Mock,
):
    # arrange
    mock_translation_adapter.translate = MagicMock()
    test_controller = controller.Controller(mock_translation_adapter)
    text = 'text'

    # act
    test_controller.submit_translation(text)

    # assert
    mock_translation_adapter.translate.assert_called_once_with(
        text=text,
    )
