from flask import abort, current_app, flash, redirect, render_template, url_for
from sqlalchemy.exc import SQLAlchemyError

from . import main
from .forms import AlunoForm
from .. import db
from ..models import Aluno, Disciplina


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/alunos', methods=['GET', 'POST'])
def alunos():
    disciplinas = db.session.scalars(
        db.select(Disciplina).order_by(Disciplina.id)
    ).all()
    form = AlunoForm()
    form.role.choices = [(disciplina.id, disciplina.nome) for disciplina in disciplinas]

    if form.validate_on_submit():
        aluno = Aluno(nome=form.name.data, disciplina_id=form.role.data)
        try:
            db.session.add(aluno)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            current_app.logger.exception('Falha ao cadastrar aluno.')
            abort(500)
        flash('Estudante cadastrado com sucesso!')
        return redirect(url_for('main.alunos'))

    alunos_cadastrados = db.session.scalars(
        db.select(Aluno).options(db.joinedload(Aluno.disciplina)).order_by(Aluno.id)
    ).all()
    return render_template(
        'alunos.html', form=form, alunos=alunos_cadastrados
    )
