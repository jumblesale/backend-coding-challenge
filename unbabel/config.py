import attr
from flask import Flask

import unbabel.controller as controller
from unbabel.blueprint import translation_page_blueprint
from unbabel.translation.test_translation_adapter import TestTranslationAdapter
from unbabel.translation.unbabel_adapter import UnbabelAdapter


@attr.s(auto_attribs=True, frozen=True)
class App:
    translation_controller: controller.Controller
    flask_app:              Flask


def _create_flask_app(
        base_url: str,
        port:     int,
        debug:    bool = False,
) -> Flask:
    app = Flask(__name__)
    app.config.update({
        'base_url': base_url,
        'debug':    debug,
        'port':     port,
    })
    app.register_blueprint(
        translation_page_blueprint
    )

    return app


def test_config():
    translation_controller = controller.Controller(
        translation_adapter=TestTranslationAdapter()
    )
    return App(
        translation_controller=translation_controller,
        flask_app=_create_flask_app(
            base_url='localhost:8888',
            port=8888,
            debug=True,
        )
    )


def dev_config():
    user_name = os.environ.get('USERNAME')
    api_key = os.environ.get('API_KEY')
    base_url = 'https://sandbox.unbabel.com/tapi/v2'
    translation_controller = controller.Controller(
        translation_adapter=UnbabelAdapter(
            user_name=user_name,
            api_key=api_key,
            base_url=base_url,
        )
    )
    return App(
        translation_controller=translation_controller,
        flask_app=_create_flask_app(
            base_url=base_url,
        )
    )
