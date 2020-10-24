from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

import os

def create_app(mode):
    app = Flask(__name__)
    app.config.from_object(mode)
    return app

app = create_app('development')


csrf = CSRFProtect(app)

db = SQLAlchemy(app)

migrate = Migrate(app, db)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login_blueprint.login'

manager = Manager(app)
manager.add_command('db', MigrateCommand)

from app.controllers.login import login_blueprint
from app.controllers.teste import teste_blueprint
app.register_blueprint(login_blueprint)
app.register_blueprint(teste_blueprint)


# from app.controllers import default
