from unittest import mock
from unittest.mock import ANY

import pytest
from hamcrest import assert_that, equal_to, contains_string, is_

from unbabel.translation import unbabel_adapter
from unbabel.types import SupportsPerformingTranslations, Uid, TranslationFailedException, Translation, StatusOption


@pytest.fixture
def mock_requests():
    with mock.patch('unbabel.translation.unbabel_adapter.requests') as m:
        yield m


@pytest.fixture
def mock_successful_post_response():
    yield mock.Mock(
        status_code=200,
        json=lambda: {"uid": 'example uid'},
    )


@pytest.fixture
def mock_successful_get_response():
    yield mock.Mock(
        status_code=200,
        json=lambda: {
            "balance":         99937.0,
            "client":          "username",
            "price":           6.0,
            "source_language": "en",
            "status":          "translating",
            "target_language": "pt",
            "text":            "Hello, world!",
            "text_format":     "text",
            "uid":             "ac1a53a264"
        }
    )


@pytest.fixture
def create_adapter():
    yield unbabel_adapter.UnbabelAdapter(
        user_name='charles',
        api_key='123xyz',
        base_url='example.com'
    )


def test_it_posts_to_url_with_headers(
        mock_requests:            mock.Mock,
        create_adapter:           SupportsPerformingTranslations,
        mock_successful_post_response: mock.Mock,
):
    # arrange
    text = 'example text'
    mock_requests.post.return_value = mock_successful_post_response

    # act
    create_adapter.translate(text=text)

    """
    Example request taken from https://developers.unbabel.com/docs/tutorial#translating-hello-world 
    """
    # assert
    mock_requests.post.assert_called_once_with(
        headers={
            'Authorization': 'ApiKey charles:123xyz',
            'Content-Type':  'application/json',
        },
        url='example.com/translation',
        data=ANY,
    )


def test_it_sends_text_to_be_translated(
    mock_requests:            mock.Mock,
    create_adapter:           SupportsPerformingTranslations,
    mock_successful_post_response: mock.Mock,
):
    # arrange
    text = 'example text'
    mock_requests.post.return_value = mock_successful_post_response

    # act
    create_adapter.translate(text=text)

    """
    From SPEC.md:
    > Build a basic web app with a simple input field that takes an English (EN) input translates it to Spanish (ES).
    we'll always go from en to es.
    """
    # assert
    mock_requests.post.assert_called_once_with(
        headers=ANY,
        url=ANY,
        data={
            'text':            text,
            'source_language': 'en',
            'target_language': 'es',
            'text_format':     'text',
        }
    )


def test_it_returns_the_response_uid_on_success(
        create_adapter: SupportsPerformingTranslations,
        mock_requests:  mock.Mock,
):
    # arrange
    text = 'example text'
    json_response = {
        "balance":         99943.0,
        "client":          "username",
        "price":           6.0,
        "source_language": "en",
        "status":          "new",
        "target_language": "pt",
        "text":            "Hello, world!",
        "text_format":     "text",
        "uid":             "ac1a53a264"
    }
    mock_response = mock.Mock(
        status_code=200,
        json=lambda: json_response
    )
    mock_requests.post.return_value = mock_response

    # act
    result = create_adapter.translate(text=text)

    # assert
    assert_that(result, equal_to(Uid('ac1a53a264')))


def test_it_throws_if_request_was_unsuccessful(
        create_adapter: SupportsPerformingTranslations,
        mock_requests:  mock.Mock,
):
    # arrange
    text = 'example text'
    mock_response = mock.Mock(
        status_code=500,
        text='error message'
    )
    mock_requests.post.return_value = mock_response

    # act
    with pytest.raises(TranslationFailedException) as e:
        create_adapter.translate(text=text)

    # assert
    assert_that(str(e), contains_string('error message'))


def test_it_gets_from_url_with_headers(
        mock_requests:                mock.Mock,
        create_adapter:               SupportsPerformingTranslations,
        mock_successful_get_response: mock.Mock,
):
    # arrange
    uid = Uid('ac1a53a264')
    mock_requests.get.return_value = mock_successful_get_response

    # act
    create_adapter.get_translation(uid=uid)

    # assert
    mock_requests.get.assert_called_once_with(
        url='example.com/translation/ac1a53a264/',
        headers={
            'Authorization': 'ApiKey charles:123xyz',
            'Content-Type': 'application/json',
        },
    )


def test_it_returns_translation_data(
        mock_requests:                mock.Mock,
        create_adapter:               SupportsPerformingTranslations,
        mock_successful_get_response: mock.Mock,
):
    # arrange
    uid = Uid('ac1a53a264')
    mock_requests.get.return_value = mock_successful_get_response

    # act
    result = create_adapter.get_translation(uid=uid)

    # assert
    assert_that(result, equal_to(Translation(
        uid=uid,
        status=StatusOption.translating,
        text='Hello, world!',
        translated_text=None,
    )))


def test_it_returns_none_if_translation_is_not_found(
        mock_requests:                mock.Mock,
        create_adapter:               SupportsPerformingTranslations,
):
    # arrange
    uid = Uid('ac1a53a264')
    mock_requests.get.return_value = mock.Mock(status_code=404)

    # act
    result = create_adapter.get_translation(uid=uid)

    # assert
    assert_that(result, is_(None))
