from unittest import mock
from unittest.mock import ANY

import pytest

from unbabel.translation import unbabel_adapter
from unbabel.types import SupportsPerformingTranslations


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
