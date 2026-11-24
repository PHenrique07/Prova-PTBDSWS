import os

import click
from flask_migrate import Migrate, upgrade

from app import create_app, db
from app.models import Aluno, Disciplina, DISCIPLINAS

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Aluno=Aluno, Disciplina=Disciplina)


@app.cli.command('init-db')
def init_db():
    """Aplica as migrações e cadastra as seis disciplinas da atividade."""
    upgrade()
    existentes = set(db.session.scalars(db.select(Disciplina.nome)).all())
    db.session.add_all(
        Disciplina(nome=nome) for nome in DISCIPLINAS if nome not in existentes
    )
    db.session.commit()
    click.echo('Banco preparado com as seis disciplinas.')


@app.cli.command()
@click.argument('test_names', nargs=-1)
def test(test_names):
    """Executa os testes da aplicação."""
    import unittest

    if test_names:
        tests = unittest.TestLoader().loadTestsFromNames(test_names)
    else:
        tests = unittest.TestLoader().discover('tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if not result.wasSuccessful():
        raise click.ClickException('Há testes com falha.')
