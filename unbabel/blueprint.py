from flask import Blueprint, render_template

translation_page_blueprint = Blueprint(
    name='blueprint',
    import_name=__name__,
    template_folder='templates'
)


@translation_page_blueprint.route('/translations')
def translation_page():
    return render_template('translation.j2')
