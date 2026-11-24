import os
from pathlib import Path

from dotenv import load_dotenv

basedir = Path(__file__).resolve().parent
load_dotenv(basedir / '.env')


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'chave-apenas-para-desenvolvimento'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    STUDENT_NAME = os.environ.get('STUDENT_NAME', 'Pedro Henrique Santos da Silva')
    STUDENT_RECORD = os.environ.get('STUDENT_RECORD', 'PT3037347')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + (basedir / 'avaliacao-dev.sqlite').as_posix()


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + (basedir / 'avaliacao.sqlite').as_posix()

    @staticmethod
    def init_app(app):
        if not os.environ.get('SECRET_KEY'):
            raise RuntimeError('Defina SECRET_KEY no arquivo .env para publicar a aplicação.')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}
