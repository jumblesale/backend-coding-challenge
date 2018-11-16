import os
from typing import Callable

from flask import Flask

from unbabel.db import db
from unbabel.controller import Controller as TranslationController
from unbabel.blueprint import create_translation_page_blueprint
from unbabel.storage.sqlalchemy.storage_adapter import SqlAlchemyStorageAdapter
from unbabel.translation.test_translation_adapter import TestTranslationAdapter
from unbabel.translation.unbabel_adapter import UnbabelAdapter
from unbabel.types import SupportsPerformingTranslations, SupportsStoringUids


def _create_flask_app(
        host:                    str,
        translation_adapter:     SupportsPerformingTranslations,
        storage_adapter_factory: Callable[[Flask], SupportsStoringUids],
        database_uri:            str,
        debug:                   bool = False,
) -> Flask:
    app = Flask(__name__)
    app.debug = debug
    app.config['SERVER_NAME'] = host
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    storage_adapter = storage_adapter_factory(app)
    app.register_blueprint(
        create_translation_page_blueprint(
            TranslationController(
                translation_adapter=translation_adapter,
                storage_adapter=storage_adapter,
            ))
    )

    return app


def test_config() -> Flask:
    return _create_flask_app(
        host='localhost:8888',
        translation_adapter=TestTranslationAdapter(),
        storage_adapter_factory=create_storage_adapter,
        database_uri=create_test_db_uri(),
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
        host='localhost:8888',
        translation_adapter=translation_adapter,
        storage_adapter_factory=create_storage_adapter,
        database_uri=create_test_db_uri(),
        debug=True,
    )


def create_test_db_uri() -> str:
    return 'postgresql://docker:docker@localhost:5555/postgres'


def create_storage_adapter(app: Flask) -> SqlAlchemyStorageAdapter:
    db.init_app(app)
    # TODO: remove this when we have migrations
    with app.app_context():
        db.drop_all()
        db.create_all()
    return SqlAlchemyStorageAdapter(db=db)
