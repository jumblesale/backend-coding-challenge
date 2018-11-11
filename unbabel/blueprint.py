from flask import Blueprint, render_template

from unbabel.controller import Controller as TranslationController


def create_translation_page_blueprint(
        translation_controller: TranslationController
) -> Blueprint:
    translation_page_blueprint = Blueprint(
        name='translation_page_blueprint',
        import_name=__name__,
        template_folder='templates'
    )

    @translation_page_blueprint.route('/')
    def translation_page():
        return render_template(
            'translation.j2',
            translations=translation_controller.get_translations(),
        )

    return translation_page_blueprint
