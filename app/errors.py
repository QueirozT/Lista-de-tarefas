from flask import current_app, Blueprint, render_template

bp_errors = Blueprint('errors', __name__)


@bp_errors.app_errorhandler(404)
def not_found_error(error):
    return render_template(
        'error.html', 
        error="Arquivo ou página não encontrado."
    ), 404


@bp_errors.app_errorhandler(500)
def internal_error(error):
    current_app.db.session.rollback()
    return render_template(
        'error.html',
        error="Um erro inesperado aconteceu."
    ), 500
