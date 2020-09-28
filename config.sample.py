import os.path

basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:SENHA@localhost/DATA_BASES'
SQLALCHEMY_TRACK_MODIFICATIONS = True  # permite modificar bd em tempo de execuçaõ
# os.path.dirname(__file__) -> diretorio atual
# basedir = os.path.abspath(os.path.dirname(__file__))  # diretório absoluto, caminho até a pasta ou arquivo atual

# SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:#planet15#@localhost/lancheriaweb'

# SQLALCHEMY_TRACK_MODIFICATIONS = True  # permite modificar bd em tempo de execução

# class Config(object):
#     DEBUG = False
#     TESTING = False
#     # CSRF_ENABLED = True
#     # SECRET_KEY = ''
#
#     SQLALCHEMY_TRACK_MODIFICATIONS = True
#
#
# class ProductionConfig(Config):
#     DEBUG = False
#
#
# class DevelopmentConfig(Config):
#     DEVELOPMENT = True
#     DEBUG = True
#
#
# class TestingConfig(Config):
#     TESTING = True
