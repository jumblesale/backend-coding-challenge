import os

from flask import Flask

from unbabel.controller import Controller as TranslationController
from unbabel.blueprint import create_translation_page_blueprint
from unbabel.translation.test_translation_adapter import TestTranslationAdapter
from unbabel.translation.unbabel_adapter import UnbabelAdapter
from unbabel.types import SupportsPerformingTranslations


def _create_flask_app(
        base_url:            str,
        translation_adapter: SupportsPerformingTranslations,
        debug:               bool = False,
) -> Flask:
    app = Flask(__name__)
    app.config.from_object({
        'HOST':  base_url,
        'DEBUG': debug,
    })
    app.register_blueprint(
        create_translation_page_blueprint(TranslationController(translation_adapter))
    )

    return app


def test_config() -> Flask:
    return _create_flask_app(
        base_url='localhost:8888',
        translation_adapter=TestTranslationAdapter(),
        debug=True,
    )


def dev_config() -> Flask:
    user_name = os.environ.get('USERNAME', '')
    api_key = os.environ.get('API_KEY', '')
    base_url = 'https://sandbox.unbabel.com/tapi/v2'
    translation_adapter = UnbabelAdapter(
        user_name=user_name,
        api_key=api_key,
        base_url=base_url,
    )
    return _create_flask_app(
        base_url=base_url,
        translation_adapter=translation_adapter,
    )
