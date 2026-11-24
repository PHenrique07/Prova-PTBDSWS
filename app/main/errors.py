from flask import render_template, request

from . import main
from .. import db

MODULOS_INDISPONIVEIS = {
    '/professores', '/disciplinas', '/cursos', '/ocorrencias',
}


@main.app_errorhandler(400)
def bad_request(error):
    return render_template('400.html'), 400


@main.app_errorhandler(404)
def page_not_found(error):
    if request.path.rstrip('/') in MODULOS_INDISPONIVEIS:
        return render_template('indisponivel.html'), 404
    return render_template('404.html'), 404


@main.app_errorhandler(500)
def internal_server_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
