from flask import Blueprint, render_template

bp = Blueprint('main', __name__)

@bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('main/404.html'), 404

@bp.app_errorhandler(500)
def internal_error(error):
    return render_template('main/500.html'), 500


@bp.route('/error')
def error():
    return render_template('main/error.html'), 400