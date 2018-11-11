from unittest import mock
from unittest.mock import ANY

import pytest
from hamcrest import assert_that, equal_to
from requests import Response

from unbabel.translation import unbabel_adapter
from unbabel.types import SupportsPerformingTranslations, Uid


@pytest.fixture
def mock_requests():
    with mock.patch('unbabel.translation.unbabel_adapter.requests') as m:
        yield m


@pytest.fixture
def create_adapter():
    yield unbabel_adapter.UnbabelAdapter(
        user_name='charles',
        api_key='123xyz',
        base_url='example.com'
    )


def test_it_posts_to_url_with_headers(
        mock_requests:  mock.Mock,
        create_adapter: SupportsPerformingTranslations,
):
    # arrange
    text = 'example text'

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
    mock_requests:  mock.Mock,
    create_adapter: SupportsPerformingTranslations,
):
    # arrange
    text = 'example text'

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
