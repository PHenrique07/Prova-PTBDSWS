import re
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from flask import Flask
from sqlalchemy.exc import SQLAlchemyError

from app import create_app, db
from app.models import Aluno, Disciplina, DISCIPLINAS


class AlunosTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.context = self.app.app_context()
        self.context.push()
        db.create_all()
        db.session.add_all(Disciplina(nome=nome) for nome in DISCIPLINAS)
        db.session.commit()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.context.pop()

    def cadastrar(self, nome='André Rufino', disciplina=3):
        response = self.client.get('/alunos')
        match = re.search(rb'name="csrf_token"[^>]*value="([^"]+)"', response.data)
        return self.client.post('/alunos', data={
            'csrf_token': match.group(1).decode(),
            'name': nome,
            'role': str(disciplina),
        }, follow_redirects=True)

    def test_identificacao_e_frameworks_na_pagina_inicial(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Pedro Henrique Santos da Silva', response.text)
        self.assertIn('PT3037347', response.text)
        self.assertIn('bootstrap', response.text)
        self.assertIn('data-timestamp=', response.text)

    def test_somente_as_duas_rotas_da_atividade(self):
        rotas = {
            regra.rule for regra in self.app.url_map.iter_rules()
            if regra.endpoint != 'static' and not regra.endpoint.startswith('bootstrap.')
        }
        self.assertEqual(rotas, {'/', '/alunos'})

    def test_as_seis_disciplinas_estao_disponiveis(self):
        response = self.client.get('/alunos')
        for nome in DISCIPLINAS:
            self.assertIn('>' + nome + '</option>', response.text)

    def test_cadastro_e_relacionamento(self):
        response = self.cadastrar()
        self.assertEqual(response.status_code, 200)
        self.assertIn('Estudante cadastrado com sucesso!', response.text)
        self.assertIn('class="alert alert-warning"', response.text)
        aluno = db.session.scalar(db.select(Aluno))
        self.assertEqual(aluno.nome, 'André Rufino')
        self.assertEqual(aluno.disciplina.nome, 'IHCA5')
        self.assertIn('André Rufino', response.text)
        self.assertIn('IHCA5', response.text)

    def test_post_redireciona_e_get_nao_repete_cadastro(self):
        self.cadastrar()
        self.client.get('/alunos')
        self.assertEqual(db.session.query(Aluno).count(), 1)

    def test_nome_vazio_ou_longo_nao_e_salvo(self):
        for nome in ('   ', 'a' * 65):
            with self.subTest(nome=nome):
                self.cadastrar(nome=nome)
                self.assertEqual(db.session.query(Aluno).count(), 0)

    def test_disciplina_inexistente_nao_e_salva(self):
        self.cadastrar(disciplina=999)
        self.assertEqual(db.session.query(Aluno).count(), 0)

    def test_post_sem_csrf_nao_cadastra(self):
        response = self.client.post('/alunos', data={'name': 'Aluno', 'role': '1'})
        self.assertIn('csrf_token', response.text)
        self.assertEqual(db.session.query(Aluno).count(), 0)

    def test_nome_exibido_com_escape_html(self):
        response = self.cadastrar(nome='<script>alert(1)</script>')
        self.assertIn('&lt;script&gt;alert(1)&lt;/script&gt;', response.text)
        self.assertNotIn('<script>alert(1)</script>', response.text)

    def test_modulos_indisponiveis(self):
        for caminho in ('professores', 'disciplinas', 'cursos', 'ocorrencias'):
            with self.subTest(caminho=caminho):
                response = self.client.get('/' + caminho)
                self.assertEqual(response.status_code, 404)
                self.assertIn('Não disponível', response.text)

    def test_pagina_inexistente(self):
        response = self.client.get('/pagina-inexistente')
        self.assertEqual(response.status_code, 404)
        self.assertIn('Página não encontrada', response.text)

    def test_erro_no_banco_desfaz_transacao(self):
        with patch.object(db.session, 'commit', side_effect=SQLAlchemyError('teste')):
            with self.assertLogs(self.app.logger, level='ERROR'):
                response = self.cadastrar()
        self.assertEqual(response.status_code, 500)
        self.assertIn('Erro interno do servidor', response.text)
        self.assertEqual(db.session.query(Aluno).count(), 0)


class PersistenciaTestCase(unittest.TestCase):
    def test_dados_sobrevivem_a_nova_instancia_da_aplicacao(self):
        with tempfile.TemporaryDirectory() as pasta:
            uri = 'sqlite:///' + (Path(pasta) / 'teste.sqlite').as_posix()
            for primeira in (True, False):
                app = Flask(__name__)
                app.config['SQLALCHEMY_DATABASE_URI'] = uri
                db.init_app(app)
                with app.app_context():
                    if primeira:
                        db.create_all()
                        disciplina = Disciplina(nome='DSWA5')
                        db.session.add(Aluno(nome='Aluno persistente', disciplina=disciplina))
                        db.session.commit()
                    else:
                        aluno = db.session.scalar(db.select(Aluno))
                        self.assertEqual(aluno.nome, 'Aluno persistente')
                        self.assertEqual(aluno.disciplina.nome, 'DSWA5')
                    db.session.remove()
                    db.engine.dispose()
