"""Entrada WSGI da aplicação no PythonAnywhere."""
from app import create_app

application = create_app('production')
