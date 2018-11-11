from flask import Blueprint, render_template, request

from unbabel.controller import Controller as TranslationController


def create_translation_page_blueprint(
        translation_controller: TranslationController
) -> Blueprint:
    translation_page_blueprint = Blueprint(
        name='translation_page_blueprint',
        import_name=__name__,
        template_folder='templates'
    )

    @translation_page_blueprint.route('/', methods=['GET'])
    def translation_page():
        return render_template(
            'translation.j2',
            translations=translation_controller.get_translations(),
        )

    @translation_page_blueprint.route('/', methods=['POST'])
    def submit_translation():
        form_data = request.form
        translation_controller.submit_translation(
            text=form_data['text']
        )
        return render_template(
            'translation.j2',
            translations=translation_controller.get_translations(),
        )

    return translation_page_blueprint
