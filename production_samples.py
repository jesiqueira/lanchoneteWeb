SECRET_KEY = '#MINHA_SENHA_SEGURA#'

TESTING = False
DEBUG = False

DRIVER = 'postgresql'
USER = 'postgres'
PASSWORD = ''
HOST = 'localhost'
BD = ''


SQLALCHEMY_DATABASE_URI = f"{DRIVER}://{USER}:{PASSWORD}@{HOST}/{BD}"
SQLALCHEMY_TRACK_MODIFICATIONS = True  # permite modificar bd em tempo de execuçaõ