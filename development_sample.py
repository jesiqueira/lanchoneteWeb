# import os.path
# basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = '#MINHA_SENHA_SEGURA#'

TESTING = True
DEBUG = True

DRIVER = 'postgresql'
USER = 'postgres'
PASSWORD = ''
HOST = 'localhost'
BD = ''


SQLALCHEMY_DATABASE_URI = f"{DRIVER}://{USER}:{PASSWORD}@{HOST}/{BD}"
SQLALCHEMY_TRACK_MODIFICATIONS = True  # permite modificar bd em tempo de execuçaõ