# Avaliação semestral — Cadastro de Alunos

**Aluno** Pedro Henrique Santos da Silva

**Prontuário** PT3037347

**Rota da avaliação** alternativa A, Cadastro de Alunos (`/alunos`)

Aplicação derivada de [PHenrique07/PTBDSWS](https://github.com/PHenrique07/PTBDSWS), com a mesma organização Flask, função `create_app`, Blueprint `main`, templates Jinja e herança de `base.html`. As versões de dependências do repositório base foram preservadas em `requirements.txt`.

## Tela inicial

![Tela inicial da aplicação](docs/tela-inicial.png)

O print foi produzido com a aplicação em execução local. A publicação no PythonAnywhere precisa ser conferida após a configuração da conta.

## Funcionalidades

- Página inicial com nome, prontuário, menu e data/hora local do navegador.
- Cadastro de aluno com nome obrigatório de até 64 caracteres e disciplina associada.
- Disciplinas DSWA5, GPSA5, IHCA5, SODA5, PJIA5 e TCOA5, persistidas no banco.
- Tabela com os alunos recuperados do banco SQLite e suas disciplinas.
- Formulário Flask-WTF com validação e token CSRF.
- Tratamento de solicitações inválidas, páginas inexistentes e erros internos.
- Links de Professores, Disciplinas, Cursos e Ocorrências exibem “Não disponível” pelo tratamento de erro 404. Apenas `/` e `/alunos` possuem rotas de aplicação, além dos arquivos estáticos do Flask e do Bootstrap.

O banco inicia com as seis disciplinas. Os alunos são inseridos pelo formulário.

## Tecnologias

Python, Flask 3.0.0, Flask-Bootstrap 3.3.7.1 (Bootstrap 3), Flask-Moment 1.0.5, Flask-WTF 1.2.1, Flask-SQLAlchemy 3.1.1, Flask-Migrate 4.0.5 e SQLite. A lista de dependências conserva também os pacotes presentes no projeto base.

## Executar no Windows

Na pasta do projeto, use o PowerShell.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m flask --app flasky init-db
.\.venv\Scripts\python.exe -m flask --app flasky run
```

Abra http://127.0.0.1:5000 e http://127.0.0.1:5000/alunos.

O comando `init-db` aplica a migração e insere as disciplinas que estiverem faltando. Pode ser executado novamente preservando os alunos cadastrados. Em desenvolvimento, os dados ficam em `avaliacao-dev.sqlite`.

## Testes

```powershell
.\.venv\Scripts\python.exe -m flask --app flasky test
```

Os testes cobrem cadastro, associação com disciplina, nomes inválidos, seleção inválida, proteção CSRF, escape de HTML, persistência em arquivo, restrição das rotas e tratamento de erros. Utilizam bancos de teste.

## Publicar no PythonAnywhere

A configuração abaixo considera o usuário **PedroSantosIFSP** e o repositório **PHenrique07/Prova-PTBDSWS**.

### 1. Preparar o projeto no console Bash

Com os arquivos publicados no GitHub, abra um console Bash do PythonAnywhere e execute os comandos abaixo. Use uma versão de Python disponível na sua conta e selecione a mesma versão na aba Web.

```bash
cd ~
git clone https://github.com/PHenrique07/Prova-PTBDSWS.git
cd Prova-PTBDSWS
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -c "import secrets; from pathlib import Path; p = Path('.env'); p.exists() or p.write_text('SECRET_KEY=' + secrets.token_hex(32) + '\n', encoding='utf-8')"
FLASK_CONFIG=production flask --app flasky init-db
```

Se o projeto já estiver clonado, entre na pasta e execute `git pull` antes de instalar as dependências e executar `init-db`.

O arquivo `.env` contém a chave usada para assinar os formulários e as sessões. Nome e prontuário já estão configurados em `config.py`. Para alterá-los, use as variáveis de `.env.example`. Em produção, os dados ficam no caminho absoluto `/home/PedroSantosIFSP/Prova-PTBDSWS/avaliacao.sqlite`.

### 2. Configurar a aba Web

1. Selecione **Add a new web app**, depois **Manual configuration** e a versão de Python usada no ambiente virtual.
2. Em **Source code** e **Working directory**, informe `/home/PedroSantosIFSP/Prova-PTBDSWS`.
3. Em **Virtualenv**, informe `/home/PedroSantosIFSP/Prova-PTBDSWS/.venv`.
4. Abra o arquivo de configuração **WSGI** indicado na aba Web e use o conteúdo abaixo.

```python
import sys

project_path = '/home/PedroSantosIFSP/Prova-PTBDSWS'
if project_path not in sys.path:
    sys.path.insert(0, project_path)

from wsgi import application
```

5. Em **Static files**, associe a URL `/static/` ao diretório `/home/PedroSantosIFSP/Prova-PTBDSWS/app/static`.
6. Clique em **Reload** e confira a página inicial, o cadastro e os links de módulos indisponíveis.

Se a conta já tiver um aplicativo Web, utilize a configuração desse aplicativo na aba Web. A entrada WSGI importa `wsgi.py`, que usa a configuração de produção.

Esse procedimento segue a [documentação oficial de Flask no PythonAnywhere](https://help.pythonanywhere.com/pages/Flask/).

## Entrega

- Repositório de destino [PHenrique07/Prova-PTBDSWS](https://github.com/PHenrique07/Prova-PTBDSWS).
- Print da tela inicial em `docs/tela-inicial.png`.
- Após publicar, conferir o domínio informado na aba Web do PythonAnywhere e preencher o formulário indicado no enunciado.
- A alternativa da questão é **A — rota [Cadastro de Alunos]**.

A licença MIT e o histórico do repositório base foram preservados.
